import { Faq } from "../components/landing/Faq";
import { Features } from "../components/landing/Features";
import { Footer } from "../components/landing/Footer";
import { Hero } from "../components/landing/Hero";
import { HowItWorks } from "../components/landing/HowItWorks";
import { Navbar } from "../components/landing/Navbar";
import { Safety } from "../components/landing/Safety";
import { Scenarios } from "../components/landing/Scenarios";
import { VoiceMode } from "../components/landing/VoiceMode";

export default function LandingPage() {
  return (
    <div className="bg-white">
      <Navbar />
      <Hero />
      <HowItWorks />
      <Features />
      <Scenarios />
      <VoiceMode />
      <Safety />
      <Faq />
      <Footer />
    </div>
  );
}
