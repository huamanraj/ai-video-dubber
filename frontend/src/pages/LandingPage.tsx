import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import {
  Film,
  Globe,
  Zap,
  Clock,
  Volume2,
  Languages,
  ArrowRight,
  CheckCircle2,
  Sparkles,
} from "lucide-react";

const FEATURES = [
  {
    icon: Globe,
    title: "10 Indian Languages",
    description: "Native support for Hindi, Bengali, Tamil, Telugu, Kannada, Malayalam, Marathi, Gujarati, Punjabi, and Odia",
  },
  {
    icon: Zap,
    title: "AI-Powered Pipeline",
    description: "Advanced speech recognition, translation, and text-to-speech using state-of-the-art AI models",
  },
  {
    icon: Clock,
    title: "Perfect Timing Sync",
    description: "Automatically adjusts dubbed audio to match original video timing with precision",
  },
  {
    icon: Volume2,
    title: "Natural Voice Options",
    description: "Choose from multiple voice models (Priya & Shubh) for authentic-sounding dubbing",
  },
];

const LANGUAGES = [
  { code: "hi", name: "Hindi", native: "हिन्दी" },
  { code: "bn", name: "Bengali", native: "বাংলা" },
  { code: "ta", name: "Tamil", native: "தமிழ்" },
  { code: "te", name: "Telugu", native: "తెలుగు" },
  { code: "kn", name: "Kannada", native: "ಕನ್ನಡ" },
  { code: "ml", name: "Malayalam", native: "മലയാളം" },
  { code: "mr", name: "Marathi", native: "मराठी" },
  { code: "gu", name: "Gujarati", native: "ગુજરાતી" },
  { code: "pa", name: "Punjabi", native: "ਪੰਜਾਬੀ" },
  { code: "or", name: "Odia", native: "ଓଡ଼ିଆ" },
];

const FAQS = [
  {
    question: "How long does the dubbing process take?",
    answer: "Processing time varies based on video length and complexity. A typical 5-minute video takes 10-15 minutes to process through all 7 pipeline stages.",
  },
  {
    question: "What video formats are supported?",
    answer: "We support all common video formats including MP4, MKV, AVI, and MOV. The output is always delivered in MP4 format for maximum compatibility.",
  },
  {
    question: "How accurate is the translation?",
    answer: "We use Google Gemini AI for context-aware translation with special handling for Indian languages, preserving tone, technical terms, and proper nouns for high accuracy.",
  },
  {
    question: "Can I choose different voices?",
    answer: "Yes! Each language offers multiple voice options including Priya (female) and Shubh (male) powered by Sarvam AI's Bulbul v3 model.",
  },
  {
    question: "What is the 7-stage pipeline?",
    answer: "Our pipeline includes: (1) Audio extraction, (2) Speech transcription, (3) Translation, (4) Text-to-speech generation, (5) Audio time-stretching, (6) Timeline assembly, and (7) Final video muxing.",
  },
  {
    question: "Is my video data secure?",
    answer: "All processing happens locally on your server. Videos are stored temporarily during processing and can be deleted after download.",
  },
];

export default function LandingPage() {
  const navigate = useNavigate();
  const [hoveredFeature, setHoveredFeature] = useState<number | null>(null);

  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-accent/20 to-background">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-grid-pattern opacity-5" />
        <div className="container mx-auto px-6 py-20 relative">
          <div className="max-w-4xl mx-auto text-center space-y-8">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium animate-pulse-subtle">
              <Sparkles className="h-4 w-4" />
              AI-Powered Video Dubbing
            </div>
            
            <h1 className="text-5xl md:text-6xl font-bold text-foreground leading-tight">
              Dub Your Videos in
              <span className="text-primary"> 10 Indian Languages</span>
            </h1>
            
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Transform your content with AI-powered dubbing. Professional quality translation and voice synthesis in minutes, not hours.
            </p>

            <div className="flex items-center justify-center gap-4 pt-4">
              <Button
                size="lg"
                onClick={() => navigate("/dashboard")}
                className="group"
              >
                Get Started
                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button
                size="lg"
                variant="outline"
                onClick={() => document.getElementById("features")?.scrollIntoView({ behavior: "smooth" })}
              >
                Learn More
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div id="features" className="container mx-auto px-6 py-20">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-foreground mb-3">
            Powerful Features
          </h2>
          <p className="text-muted-foreground">
            Everything you need for professional video dubbing
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          {FEATURES.map((feature, index) => (
            <Card
              key={index}
              className="relative overflow-hidden transition-all duration-300 hover:shadow-elevated cursor-pointer"
              onMouseEnter={() => setHoveredFeature(index)}
              onMouseLeave={() => setHoveredFeature(null)}
            >
              <CardContent className="p-6 space-y-3">
                <div
                  className={`inline-flex p-3 rounded-lg bg-primary/10 text-primary transition-transform duration-300 ${
                    hoveredFeature === index ? "scale-110" : ""
                  }`}
                >
                  <feature.icon className="h-6 w-6" />
                </div>
                <h3 className="font-semibold text-foreground">{feature.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Languages Section */}
      <div className="bg-accent/30 py-20">
        <div className="container mx-auto px-6">
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-2 mb-4">
              <Languages className="h-6 w-6 text-primary" />
              <h2 className="text-3xl font-bold text-foreground">
                Supported Languages
              </h2>
            </div>
            <p className="text-muted-foreground">
              Native support for major Indian languages
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 max-w-4xl mx-auto">
            {LANGUAGES.map((lang, index) => (
              <Card
                key={lang.code}
                className="text-center hover:shadow-card transition-all duration-300 hover:-translate-y-1"
                style={{
                  animationDelay: `${index * 50}ms`,
                }}
              >
                <CardContent className="p-4 space-y-1">
                  <div className="text-2xl font-semibold text-foreground">
                    {lang.native}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {lang.name}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div className="container mx-auto px-6 py-20">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-foreground mb-3">
            How It Works
          </h2>
          <p className="text-muted-foreground">
            Simple 7-stage pipeline for professional results
          </p>
        </div>

        <div className="max-w-3xl mx-auto space-y-4">
          {[
            { stage: 1, title: "Extract Audio", desc: "Separate audio from video" },
            { stage: 2, title: "Transcribe Speech", desc: "Convert speech to text with timestamps" },
            { stage: 3, title: "Translate Content", desc: "AI-powered contextual translation" },
            { stage: 4, title: "Generate Speech", desc: "Natural voice synthesis in target language" },
            { stage: 5, title: "Sync Timing", desc: "Match dubbed audio to original timing" },
            { stage: 6, title: "Build Timeline", desc: "Assemble complete audio track" },
            { stage: 7, title: "Finalize Video", desc: "Merge dubbed audio with original video" },
          ].map((step) => (
            <Card key={step.stage} className="hover:shadow-card transition-shadow">
              <CardContent className="p-4 flex items-center gap-4">
                <div className="flex-shrink-0 w-10 h-10 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-semibold">
                  {step.stage}
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground">{step.title}</h4>
                  <p className="text-sm text-muted-foreground">{step.desc}</p>
                </div>
                <CheckCircle2 className="h-5 w-5 text-primary" />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Voice Models */}
      <div className="bg-accent/30 py-20">
        <div className="container mx-auto px-6">
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-2 mb-4">
              <Volume2 className="h-6 w-6 text-primary" />
              <h2 className="text-3xl font-bold text-foreground">
                Voice Models
              </h2>
            </div>
            <p className="text-muted-foreground">
              Powered by Sarvam AI Bulbul v3 - 37 unique voices
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            <Card className="hover:shadow-elevated transition-shadow">
              <CardContent className="p-8 text-center space-y-4">
                <div className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center mx-auto">
                  <Volume2 className="h-10 w-10 text-primary" />
                </div>
                <h3 className="text-2xl font-semibold text-foreground">37 Professional Voices</h3>
                <p className="text-muted-foreground max-w-2xl mx-auto">
                  Choose from a diverse range of natural-sounding voices including Shubh, Priya, Aditya, Ritu, Neha, Rahul, and many more. Each voice is optimized for clarity and authenticity across all supported languages.
                </p>
                <div className="pt-4 flex flex-wrap justify-center gap-2 text-sm text-muted-foreground">
                  {["Shubh", "Priya", "Aditya", "Ritu", "Neha", "Rahul", "Pooja", "Rohan", "Simran", "Kavya", "Amit", "Dev"].map((voice) => (
                    <span key={voice} className="px-3 py-1 bg-accent rounded-full">
                      {voice}
                    </span>
                  ))}
                  <span className="px-3 py-1 bg-primary/10 text-primary rounded-full font-medium">
                    +25 more
                  </span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* FAQ Section */}
      <div className="container mx-auto px-6 py-20">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-foreground mb-3">
            Frequently Asked Questions
          </h2>
          <p className="text-muted-foreground">
            Everything you need to know about our dubbing service
          </p>
        </div>

        <div className="max-w-3xl mx-auto">
          <Accordion type="single" collapsible className="space-y-4">
            {FAQS.map((faq, index) => (
              <AccordionItem
                key={index}
                value={`item-${index}`}
                className="border rounded-lg px-6 bg-card"
              >
                <AccordionTrigger className="text-left hover:no-underline py-4">
                  <span className="font-semibold text-foreground">{faq.question}</span>
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground pb-4">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-primary/5 py-20">
        <div className="container mx-auto px-6 text-center">
          <div className="max-w-2xl mx-auto space-y-6">
            <h2 className="text-3xl font-bold text-foreground">
              Ready to Transform Your Videos?
            </h2>
            <p className="text-lg text-muted-foreground">
              Start dubbing your content in multiple Indian languages today
            </p>
            <Button
              size="lg"
              onClick={() => navigate("/dashboard")}
              className="group"
            >
              Launch Dashboard
              <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
            </Button>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="container mx-auto px-6 text-center text-sm text-muted-foreground">
          <div className="flex items-center justify-center gap-2 mb-2">
            <Film className="h-4 w-4 text-primary" />
            <span className="font-semibold text-foreground">DubStudio</span>
          </div>
          <p>AI-Powered Video Dubbing Platform</p>
        </div>
      </footer>
    </div>
  );
}
