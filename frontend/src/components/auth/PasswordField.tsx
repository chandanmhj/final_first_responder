import { useState, type InputHTMLAttributes } from "react";
import { Input } from "../ui/Input";

type Props = Omit<InputHTMLAttributes<HTMLInputElement>, "type"> & {
  label?: string;
  error?: string;
  hint?: string;
};

/** Password input with a show/hide toggle. */
export function PasswordField({ label = "Password", ...rest }: Props) {
  const [visible, setVisible] = useState(false);
  return (
    <Input
      {...rest}
      label={label}
      type={visible ? "text" : "password"}
      trailing={
        <button
          type="button"
          onClick={() => setVisible((v) => !v)}
          aria-label={visible ? "Hide password" : "Show password"}
          className="rounded-lg px-2 py-1 text-xs font-semibold text-brand-600 hover:bg-brand-50"
        >
          {visible ? "Hide" : "Show"}
        </button>
      }
    />
  );
}
