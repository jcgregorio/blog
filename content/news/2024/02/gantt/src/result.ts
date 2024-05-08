/** Result allows easier handling of returning either an error or a value from a
 * function. */
export type Result<T> = { ok: true; value: T } | { ok: false; error: Error };

export function ok<T>(value: T): Result<T> {
  return { ok: true, value: value };
}

export function error<T>(value: string | Error): Result<T> {
  if (typeof value === "string") {
    return { ok: false, error: new Error(value) };
  }
  return { ok: false, error: value };
}
