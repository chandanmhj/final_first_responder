import { forwardRef, useId, type InputHTMLAttributes, type ReactNode } from "react";

type Props = InputHTMLAttributes<HTMLInputElement> & {
  label: string;
  error?: string;
  hint?: string;
  trailing?: ReactNode;
};

/** Labelled text input with error and hint text. */
export const Input = forwardRef<HTMLInputElement, Props>(function Input(
  { label, error, hint, trailing, id, className = "", ...rest },
  ref,
) {
  const auto = useId();
  const inputId = id ?? auto;
  const describedBy = error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined;
  return (
    <div className="space-y-1.5">
      <label htmlFor={inputId} className="block text-sm font-medium text-ink-700">
        {label}
      </label>
      <div className="relative">
        <input
          {...rest}
          ref={ref}
          id={inputId}
          aria-invalid={error ? true : undefined}
          aria-describedby={describedBy}
          className={`h-11 w-full rounded-xl border bg-white px-3.5 text-sm text-ink-900 placeholder:text-ink-300 transition-colors focus:border-brand-500 focus:outline-none focus:ring-4 focus:ring-brand-100 ${error ? "border-emergency-500" : "border-ink-200"} ${trailing ? "pr-16" : ""} ${className}`}
        />
        {trailing && <div className="absolute inset-y-0 right-2 flex items-center">{trailing}</div>}
      </div>
      {error ? (
        <p id={`${inputId}-error`} className="text-xs text-emergency-600">{error}</p>
      ) : hint ? (
        <p id={`${inputId}-hint`} className="text-xs text-ink-500">{hint}</p>
      ) : null}
    </div>
  );
});
