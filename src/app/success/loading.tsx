export default function SuccessLoading() {
  return (
    <div className="pt-20 pb-24">
      <div className="max-w-content mx-auto px-6">
        <div className="max-w-xl mx-auto text-center">
          <div className="inline-block w-6 h-6 border-2 border-border border-t-primary rounded-full animate-spin mb-6" />
          <p className="text-body text-secondary">
            Confirming your order...
          </p>
        </div>
      </div>
    </div>
  );
}
