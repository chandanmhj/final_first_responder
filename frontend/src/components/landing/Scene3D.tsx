import { useEffect, useRef } from "react";
import * as THREE from "three";

const RED = 0xe5383b;
const BLUE = 0x3b73f0;

function heartShape(): THREE.Shape {
  const s = new THREE.Shape();
  s.moveTo(0.25, 0.25);
  s.bezierCurveTo(0.25, 0.25, 0.2, 0, 0, 0);
  s.bezierCurveTo(-0.3, 0, -0.3, 0.35, -0.3, 0.35);
  s.bezierCurveTo(-0.3, 0.55, -0.15, 0.77, 0.25, 0.95);
  s.bezierCurveTo(0.6, 0.77, 0.8, 0.55, 0.8, 0.35);
  s.bezierCurveTo(0.8, 0.35, 0.8, 0, 0.5, 0);
  s.bezierCurveTo(0.35, 0, 0.25, 0.25, 0.25, 0.25);
  return s;
}

function makeCross(): THREE.Group {
  const g = new THREE.Group();
  const mat = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0x3b73f0, emissiveIntensity: 0.6, roughness: 0.3 });
  g.add(new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.14, 0.14), mat));
  g.add(new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.5, 0.14), mat));
  return g;
}

/** lub-dub: two quick pulses per beat, 0..1 */
function beat(t: number): number {
  const p = (t % 1.15) / 1.15;
  return Math.exp(-(((p - 0.08) / 0.05) ** 2)) + 0.6 * Math.exp(-(((p - 0.28) / 0.06) ** 2));
}

/** The 3D hero: a beating glossy heart with ripples, orbits, crosses and particles. Reacts to the pointer and to scrolling. */
export default function Scene3D() {
  const mount = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = mount.current;
    if (!el) return;
    let renderer: THREE.WebGLRenderer;
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: "high-performance" });
    } catch {
      return; // no WebGL: the CSS background still looks fine
    }
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x000000, 0);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;
    el.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
    camera.position.set(0, 0, 9);

    scene.add(new THREE.AmbientLight(0xffffff, 0.7));
    const key = new THREE.DirectionalLight(0xffffff, 2.4);
    key.position.set(3, 5, 6);
    const fill = new THREE.DirectionalLight(BLUE, 2.2);
    fill.position.set(-6, -1, 3);
    const rim = new THREE.DirectionalLight(RED, 2.0);
    rim.position.set(5, -3, -4);
    scene.add(key, fill, rim);

    const world = new THREE.Group();
    scene.add(world);
    const heartG = new THREE.Group();
    world.add(heartG);

    // heart
    const geo = new THREE.ExtrudeGeometry(heartShape(), { depth: 0.28, bevelEnabled: true, bevelThickness: 0.16, bevelSize: 0.14, bevelSegments: 10, curveSegments: 56 });
    geo.center();
    const heartMat = new THREE.MeshPhysicalMaterial({ color: RED, roughness: 0.22, metalness: 0.15, clearcoat: 1, clearcoatRoughness: 0.12, emissive: 0x8a1015, emissiveIntensity: 0.4 });
    const heart = new THREE.Mesh(geo, heartMat);
    heart.scale.setScalar(3.1);
    heartG.add(heart);

    // soft glow behind the heart
    const c = document.createElement("canvas");
    c.width = c.height = 256;
    const cx = c.getContext("2d");
    if (cx) {
      const g = cx.createRadialGradient(128, 128, 0, 128, 128, 128);
      g.addColorStop(0, "rgba(229,56,59,0.55)");
      g.addColorStop(0.45, "rgba(59,115,240,0.18)");
      g.addColorStop(1, "rgba(59,115,240,0)");
      cx.fillStyle = g;
      cx.fillRect(0, 0, 256, 256);
    }
    const glowTex = new THREE.CanvasTexture(c);
    const glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));
    glow.scale.setScalar(11);
    glow.position.z = -1.2;
    heartG.add(glow);

    // ripples
    const ripples: THREE.Mesh[] = [0, 1, 2].map(() => {
      const m = new THREE.Mesh(new THREE.RingGeometry(1.5, 1.56, 96), new THREE.MeshBasicMaterial({ color: 0x9db8ff, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide }));
      m.position.z = -0.4;
      heartG.add(m);
      return m;
    });

    // orbits with satellites
    const orbits = [
      { r: 3.1, tilt: 1.15, color: BLUE, speed: 0.5 },
      { r: 3.9, tilt: -0.7, color: RED, speed: -0.32 },
    ].map((o) => {
      const g = new THREE.Group();
      g.rotation.x = o.tilt;
      g.add(new THREE.Mesh(new THREE.TorusGeometry(o.r, 0.012, 8, 160), new THREE.MeshBasicMaterial({ color: o.color, transparent: true, opacity: 0.5 })));
      const sat = new THREE.Mesh(new THREE.SphereGeometry(0.11, 24, 24), new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: o.color, emissiveIntensity: 1.4 }));
      sat.position.x = o.r;
      const pivot = new THREE.Group();
      pivot.add(sat);
      g.add(pivot);
      heartG.add(g);
      return { pivot, speed: o.speed };
    });

    // floating medical crosses
    const crosses = Array.from({ length: 7 }, (_, i) => {
      const m = makeCross();
      const a = (i / 7) * Math.PI * 2 + 0.4;
      const r = 4.6 + (i % 3) * 0.7;
      m.position.set(Math.cos(a) * r, Math.sin(a) * r * 0.62, -1.5 + (i % 4) * 0.9);
      m.scale.setScalar(0.5 + (i % 3) * 0.2);
      world.add(m);
      return { m, base: m.position.y, phase: i * 1.3 };
    });

    // particles
    const N = window.innerWidth < 640 ? 260 : 700;
    const pos = new Float32Array(N * 3);
    for (let i = 0; i < N; i++) {
      const r = 5 + Math.random() * 9;
      const th = Math.random() * Math.PI * 2;
      const ph = Math.acos(2 * Math.random() - 1);
      pos.set([r * Math.sin(ph) * Math.cos(th), r * Math.sin(ph) * Math.sin(th) * 0.7, r * Math.cos(ph) - 2], i * 3);
    }
    const pg = new THREE.BufferGeometry();
    pg.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    const particles = new THREE.Points(pg, new THREE.PointsMaterial({ color: 0x9db8ff, size: 0.045, transparent: true, opacity: 0.85, depthWrite: false, blending: THREE.AdditiveBlending }));
    world.add(particles);

    // sizing and layout: heart sits to the right on wide screens, above the text on narrow ones
    let aspect = 1;
    const layout = () => {
      const w = el.clientWidth || 1;
      const h = el.clientHeight || 1;
      aspect = w / h;
      renderer.setSize(w, h, false);
      renderer.domElement.style.width = "100%";
      renderer.domElement.style.height = "100%";
      camera.aspect = aspect;
      camera.updateProjectionMatrix();
      const wide = aspect > 1.3;
      heartG.position.set(wide ? 2.7 : 0, wide ? 0 : 2.2, 0);
      heartG.scale.setScalar(wide ? 1 : 0.62);
    };
    layout();
    const ro = new ResizeObserver(layout);
    ro.observe(el);

    const mouse = { x: 0, y: 0 };
    const cur = { x: 0, y: 0 };
    let scroll = 0;
    const onMove = (e: PointerEvent) => { mouse.x = (e.clientX / window.innerWidth) * 2 - 1; mouse.y = (e.clientY / window.innerHeight) * 2 - 1; };
    const onScroll = () => { scroll = Math.min(window.scrollY / window.innerHeight, 1.5); };
    window.addEventListener("pointermove", onMove, { passive: true });
    window.addEventListener("scroll", onScroll, { passive: true });

    let visible = true;
    const io = new IntersectionObserver(([e]) => { visible = !!e?.isIntersecting; });
    io.observe(el);

    const clock = new THREE.Clock();
    let raf = 0;
    const render = (t: number) => {
      const b = beat(t);
      heart.scale.setScalar(3.1 * (1 + 0.075 * b));
      heartMat.emissiveIntensity = 0.35 + 1.1 * b;
      ripples.forEach((r, i) => {
        const p = ((t + i * 0.75) % 2.25) / 2.25;
        r.scale.setScalar(1 + p * 1.9);
        (r.material as THREE.MeshBasicMaterial).opacity = (1 - p) * 0.35;
      });
      orbits.forEach((o) => { o.pivot.rotation.z = t * o.speed; });
      crosses.forEach((c2) => {
        c2.m.position.y = c2.base + Math.sin(t * 0.8 + c2.phase) * 0.35;
        c2.m.rotation.x = t * 0.4 + c2.phase;
        c2.m.rotation.y = t * 0.55 + c2.phase;
      });
      particles.rotation.y = t * 0.025;
      // smooth pointer parallax and scroll
      cur.x += (mouse.x - cur.x) * 0.05;
      cur.y += (mouse.y - cur.y) * 0.05;
      heartG.rotation.y = cur.x * 0.5 + Math.sin(t * 0.4) * 0.12;
      heartG.rotation.x = cur.y * 0.3;
      world.rotation.y = cur.x * 0.08;
      world.position.y = scroll * 1.6;
      camera.position.z = 9 + scroll * 3.5;
      camera.position.x += (cur.x * 0.6 - camera.position.x) * 0.04;
      camera.lookAt(0, 0, 0);
      renderer.render(scene, camera);
    };
    const tick = () => {
      raf = requestAnimationFrame(tick);
      if (visible) render(clock.getElapsedTime());
    };
    if (reduce) render(0.1);
    else tick();

    return () => {
      cancelAnimationFrame(raf);
      ro.disconnect();
      io.disconnect();
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("scroll", onScroll);
      scene.traverse((o) => {
        const m = o as THREE.Mesh;
        m.geometry?.dispose();
        const mat = m.material;
        if (Array.isArray(mat)) mat.forEach((x) => x.dispose());
        else mat?.dispose();
      });
      glowTex.dispose();
      renderer.dispose();
      renderer.forceContextLoss();
      renderer.domElement.remove();
    };
  }, []);

  return <div ref={mount} className="absolute inset-0" aria-hidden="true" />;
}