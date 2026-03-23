interface EquationLabelProps {
  equation: string;
  className?: string;
}

export default function EquationLabel({
  equation,
  className = "",
}: EquationLabelProps) {
  return (
    <p
      className={`font-mono text-caption tracking-wider text-secondary ${className}`}
    >
      {equation}
    </p>
  );
}
