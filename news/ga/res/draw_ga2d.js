this.draw_ga2d = this.ga2d_draw || function() {
  var g = ga2d;
  var d = {};

  // We'll presume vectors are passed in as members of G^2.
  class Frame {
    constructor(canvas) {
      this.canvas = canvas;
      this.ops = [];
      this.extent = {
        maxx: 0;
        maxy: 0;
        minx: 0;
        miny: 0;
      };
    }

    vec(v, label) {
      this.updateExtents(v);
      // Add to list of ops.
    }

    updateExtents(v) {
      if (v[1] > this.extent.maxx) {
        this.extent.maxx = v[1];
      }
      if (v[1] < this.extent.minx) {
        this.extent.minx = v[1];
      }
      if (v[2] > this.extent.maxy) {
        this.extent.maxy = v[2];
      }
      if (v[2] < this.extent.miny) {
        this.extent.miny = v[2];
      }
    }

    draw() {
    }
  }
