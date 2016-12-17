this.ga2d = this.ga2d || function() {
  var ga2d = {};

  // Library for manipulating 2-D vectors using Geometric Algebra.
  //
  // Each element of the 2-D GA space will be represented as a vector
  // or 4 numbers, representing:
  //
  //   \bar{x} = a + b e_{1} + c e_{2} + d e_{12}
  //
  // will have in interal representation of:
  //
  //    [a, b, c, d].
  //
  // The first thing to do is define the Geometric Product of such
  // elements.
  //
  ga2d.mul = function(x, y) {
    return [
      x[0]*y[0] + x[1]*y[1] + x[2]*y[2] - x[3]*y[3],
      x[0]*y[1] + x[1]*y[0] - x[2]*y[3] + x[3]*y[2],
      x[0]*y[2] + x[2]*y[0] + x[1]*y[3] - x[3]*y[1],
      x[0]*y[3] + x[3]*y[0] + x[1]*y[2] - x[2]*y[1]
    ]
  };

  ga2d.add = function(x, y) {
    return [
      x[0] + y[0],
      x[1] + y[1],
      x[2] + y[2],
      x[3] + y[3]
    ]
  };

  ga2d.sub = function(x, y) {
    return [
      x[0] - y[0],
      x[1] - y[1],
      x[2] - y[2],
      x[3] - y[3]
    ]
  };


  ga2d.inv = function(x) {
    if (x[0] !== 0 || x[3] !== 0) {
      throw "Can only invert vectors.";
    }
    var norm = x[1]*x[1] + x[2]*x[2];
    return [
      0,
      x[1]/norm,
      x[2]/norm,
      0
    ];
  };

  ga2d.norm = function(x) {
    if (x[0] !== 0 || x[3] !== 0) {
      throw "Can only invert vectors.";
    }
    var norm = Math.sqrt(x[1]*x[1] + x[2]*x[2]);
    return [
      0,
      x[1]/norm,
      x[2]/norm,
      0
    ];
  }


  // vec turns a vector <x, y> into an element of the 2-D GA space.
  ga2d.vec = function(x, y) {
    return [0, x, y, 0];
  }

  ga2d.scalar = function(c) {
    return [c, 0, 0, 0];
  }

  ga2d.e = function(theta) {
    return [Math.cos(theta), 0, 0, Math.sin(theta)];
  }

  return ga2d;
}();
