interface TestimonialProps {
  quote: string;
  author: string;
  role?: string;
}

export default function Testimonial({ quote, author, role }: TestimonialProps) {
  return (
    <blockquote className="border-l-2 border-border pl-6 py-2">
      <p className="text-body text-secondary italic mb-2">
        &ldquo;{quote}&rdquo;
      </p>
      <footer className="text-caption text-muted">
        &mdash; {author}
        {role && <span>, {role}</span>}
      </footer>
    </blockquote>
  );
}
