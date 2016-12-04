this.draw_ga2d = this.ga2d_draw || function() {
  var g = ga2d;
  var d = {};

  // We'll presume vectors are passed in as members of G^2.
  class Frame {
    constructor(canvas) {
      this.canvas = canvas;
      this.ctx = canvas.getContext('2d');

      this.ctx.font = "bold 18px serif";
      this.ops = [];
      this.extent = {
        max: 0,
        min: 0,
      };
    }

    vec(v, label) {
      this._updateExtents(v);
      // Add to list of ops.
      this.ops.push({
        op: "vec",
        value: v,
        offset: [0, 0, 0, 0],
        label: label,
      });
    }

    vecFrom(v, offset, label) {
      this._updateExtents(v);
      this._updateExtents(g.add(v, offset));
      // Add to list of ops.
      this.ops.push({
        op: "vec",
        value: v,
        offset: offset,
        label: label,
      });
    }

    axes() {
      this.ops.push({
        op: "axes",
      });
    }

    _updateExtents(v) {
      if (v[1] > this.extent.max) {
        this.extent.max = v[1];
      }
      if (-v[1] > this.extent.max) {
        this.extent.max= -v[1];
      }
      if (v[2] > this.extent.max) {
        this.extent.max = v[2];
      }
      if (-v[2] > this.extent.max) {
        this.extent.max = -v[2];
      }
    }

    _moveto(pt) {
      this.ctx.moveTo(pt[0], pt[1]);
    }

    _lineto(pt) {
      this.ctx.lineTo(pt[0], pt[1]);
    }

    _text(pt, label) {
      this.ctx.fillText(label, pt[0], pt[1]);
    }

    draw() {
      var css_extent = this.canvas.height;
      var source_extent = 1.2 * (2*this.extent.max);
      var origin = source_extent/2;
      var ratio = (css_extent/source_extent);
      var rotPi = [-1, 0, 0, 0];
      var mid = [0.5, 0, 0, 0];
      var xform = function(v) {
        return [(v[1]+origin)*ratio, (-v[2]+origin)*ratio];
      }
      this.ops.forEach(function(op) {
        if (op.op === "vec") {
          this.ctx.beginPath();
          this.ctx.strokeStyle = "#000";
          this._moveto(xform(op.offset));
          var source_tip = g.add(op.value, op.offset);
          var tip = xform(source_tip);
          this._lineto(tip);

          // Draw arrow heads.
          var rev = g.mul([0.2, 0, 0, 0], g.mul(g.norm(op.value), rotPi));
          var left = g.mul(rev, g.e(Math.PI/10));
          this._moveto(tip);
          this._lineto(xform(g.add(source_tip, left)));

          var right= g.mul(rev, g.e(-Math.PI/10));
          this._moveto(tip);
          this._lineto(xform(g.add(source_tip, right)));

          this.ctx.stroke();

          // Draw label.
          var m = g.mul(mid, op.value);
          var ortho = g.mul([0.3, 0, 0, 0], g.mul(g.norm(op.value), g.e(-Math.PI/2)));
          var textLoc = g.add(op.offset, g.add(m, ortho));
          this._text(xform(textLoc), op.label)
        } else if (op.op == "axes") {
          this.ctx.beginPath();
          this.ctx.strokeStyle = "#ddd";
          this.ctx.moveTo(0, css_extent/2);
          this.ctx.lineTo(css_extent, css_extent/2);
          this.ctx.moveTo(css_extent/2, 0);
          this.ctx.lineTo(css_extent/2, css_extent);
          this.ctx.stroke();
        }
      }.bind(this));
    }
  }

  d.Frame = Frame;

  return d;
}();
