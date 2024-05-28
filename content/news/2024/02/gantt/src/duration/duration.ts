/** Simulates the expected distribution of durations.
 *
 *  Note that we can create quartiles from this by feeding in the values [0.25,
 *  0.5, 0.75].
 */
export interface DurationModel {
  // Input is the task duration, and a number in the range [0,1] and is passed
  // into the inverse CDF for durations. Implementations should memoize the CDF
  // based on the passed in duration.
  sample(duration: number, p: number): number;

  // Serializes the Model to JSON. Note that it MUST serialize the class name of
  // the DurationModel implementation in the 'ctor' value of the returned
  // object. Unless that's not needed and we store the ctor as part of the
  // Chart?
  toJSON(key: string): object;
}
