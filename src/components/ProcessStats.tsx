import { allPieces, series } from "@/data/series";

export default function ProcessStats() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-8">
      {[
        { number: "200+", label: "renders made across all series" },
        { number: String(allPieces.length), label: "pieces that survived curation" },
        { number: String(series.length), label: "human emotions explored" },
        { number: "100s", label: "of hours of mathematical research" },
        { number: "0", label: "AI image generators used" },
        { number: "300 DPI", label: "print resolution on every file" },
      ].map((stat) => (
        <div key={stat.label}>
          <p className="text-2xl md:text-3xl font-mono font-light text-primary">
            {stat.number}
          </p>
          <p className="text-caption text-secondary mt-1">{stat.label}</p>
        </div>
      ))}
    </div>
  );
}
