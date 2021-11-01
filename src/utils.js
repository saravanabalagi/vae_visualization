export const getStd = (array) => {
  const n = array.length;
  if (n === 0) return 0;
  const mean = array.reduce((a, b) => a + b) / n;
  return Math.sqrt(
    array.map((x) => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / n
  );
};

export const getMean = (array) =>
  array.reduce((a, b) => a + b, 0) / array.length;

// Standard Normal variate using Box-Muller transform.
export const getRandn = () => {
  let u = 0,
    v = 0;
  while (u === 0) u = Math.random(); //Converting [0,1) to (0,1)
  while (v === 0) v = Math.random();
  return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
};

export const getLNorm = (array, l = 2, eps = 1e-6) => {
    if (l === 0) return array.reduce((acc, v) => (Math.abs(v) < eps) ? acc : acc + 1, 0);
    if (l === 1) return array.reduce((acc,v) => acc + Math.abs(v), 0);
    if (l === Infinity) return Math.max(...array.map(e => Math.abs(e)));
    return array.reduce((acc,v) => acc + Math.pow(v, l), 0);
}

export const isObj = (obj) => {
    return typeof obj === 'object' && obj !== null;
};
