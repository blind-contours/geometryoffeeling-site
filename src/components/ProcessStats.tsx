import { allPieces, series } from "@/data/series";

export default function ProcessStats() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
      {[
        { number: "Thousands", label: "of renders across all series" },
        { number: String(allPieces.length), label: "pieces that survived curation" },
        { number: String(series.length), label: "human emotions explored" },
        { number: "100s", label: "of hours of mathematical research" },
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
