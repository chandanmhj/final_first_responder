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

/** lub-dub: two quick pulses per beat, 0..1 */
function beat(t: number): number {
  const p = (t % 1.15) / 1.15;
  return Math.exp(-(((p - 0.08) / 0.05) ** 2)) + 0.6 * Math.exp(-(((p - 0.28) / 0.06) ** 2));
}

/** Simple 3D hero: one glossy beating heart, soft glow, two ripples, one orbit and a few particles. Phone-first. */
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
    const coarse = window.matchMedia("(pointer: coarse)").matches; // phones and tablets
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, coarse ? 1.5 : 2));
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

    // heart (upright)
    const geo = new THREE.ExtrudeGeometry(heartShape(), { depth: 0.28, bevelEnabled: true, bevelThickness: 0.16, bevelSize: 0.14, bevelSegments: coarse ? 6 : 10, curveSegments: coarse ? 36 : 56 });
    geo.rotateZ(Math.PI);
    geo.center();
    const heartMat = new THREE.MeshPhysicalMaterial({ color: RED, roughness: 0.22, metalness: 0.15, clearcoat: 1, clearcoatRoughness: 0.12, emissive: 0x8a1015, emissiveIntensity: 0.4 });
    const heart = new THREE.Mesh(geo, heartMat);
    heart.scale.setScalar(3.1);
    heartG.add(heart);

    // soft glow
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
    glow.scale.setScalar(10);
    glow.position.z = -1.2;
    heartG.add(glow);

    // two ripples
    const ripples: THREE.Mesh[] = [0, 1].map(() => {
      const m = new THREE.Mesh(new THREE.RingGeometry(1.5, 1.55, 96), new THREE.MeshBasicMaterial({ color: 0x9db8ff, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide }));
      m.position.z = -0.4;
      heartG.add(m);
      return m;
    });

    // one thin orbit with a glowing satellite
    const orbit = new THREE.Group();
    orbit.rotation.x = 1.15;
    orbit.add(new THREE.Mesh(new THREE.TorusGeometry(3.1, 0.01, 8, 160), new THREE.MeshBasicMaterial({ color: BLUE, transparent: true, opacity: 0.4 })));
    const pivot = new THREE.Group();
    const sat = new THREE.Mesh(new THREE.SphereGeometry(0.11, 20, 20), new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: BLUE, emissiveIntensity: 1.4 }));
    sat.position.x = 3.1;
    pivot.add(sat);
    orbit.add(pivot);
    heartG.add(orbit);

    // a few particles
    const N = coarse ? 140 : 320;
    const pos = new Float32Array(N * 3);
    for (let i = 0; i < N; i++) {
      const r = 5 + Math.random() * 8;
      const th = Math.random() * Math.PI * 2;
      const ph = Math.acos(2 * Math.random() - 1);
      pos.set([r * Math.sin(ph) * Math.cos(th), r * Math.sin(ph) * Math.sin(th) * 0.8, r * Math.cos(ph) - 2], i * 3);
    }
    const pg = new THREE.BufferGeometry();
    pg.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    const particles = new THREE.Points(pg, new THREE.PointsMaterial({ color: 0x9db8ff, size: coarse ? 0.06 : 0.045, transparent: true, opacity: 0.8, depthWrite: false, blending: THREE.AdditiveBlending }));
    world.add(particles);

    // layout: portrait (phones) puts the heart in the upper part, above the text; wide screens put it on the right
    const layout = () => {
      const w = el.clientWidth || 1;
      const h = el.clientHeight || 1;
      const aspect = w / h;
      renderer.setSize(w, h, false);
      renderer.domElement.style.width = "100%";
      renderer.domElement.style.height = "100%";
      camera.aspect = aspect;
      camera.updateProjectionMatrix();
      if (aspect < 1.1) {
        heartG.position.set(0, 1.55, 0);
        heartG.scale.setScalar(aspect < 0.6 ? 0.7 : 0.85);
      } else {
        heartG.position.set(aspect > 1.3 ? 2.7 : 1.8, 0, 0);
        heartG.scale.setScalar(1);
      }
    };
    layout();
    const ro = new ResizeObserver(layout);
    ro.observe(el);

    // touch drag or mouse move tilts the heart gently
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
        const p = ((t + i * 1.1) % 2.25) / 2.25;
        r.scale.setScalar(1 + p * 1.9);
        (r.material as THREE.MeshBasicMaterial).opacity = (1 - p) * 0.3;
      });
      pivot.rotation.z = t * 0.5;
      particles.rotation.y = t * 0.025;
      cur.x += (mouse.x - cur.x) * 0.05;
      cur.y += (mouse.y - cur.y) * 0.05;
      heartG.rotation.y = Math.sin(t * 0.5) * 0.3 + cur.x * 0.45; // always swaying, so it feels alive without input
      heartG.rotation.x = cur.y * 0.25;
      world.position.y = scroll * 1.6;
      camera.position.z = 9 + scroll * 3;
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