import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <div className="grid min-h-dvh place-items-center px-5 text-center">
      <div>
        <p className="font-display text-6xl font-extrabold text-brand-600">404</p>
        <h1 className="mt-3 text-2xl font-bold text-ink-950">This page doesn't exist</h1>
        <Link to="/" className="mt-6 inline-block font-semibold text-brand-600 hover:underline">Go to the home page</Link>
      </div>
    </div>
  );
}
