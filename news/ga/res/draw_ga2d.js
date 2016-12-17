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
        xmax: 0,
        xmin: 0,
        ymax: 0,
        ymin: 0,
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

    expandTo(v) {
      this._updateExtents(v);
    }

    clear() {
      this.ctx.clearRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
      this.ops = [];
    }

    region(ar, label, color) {
      ar.forEach(function(v) {
        this._updateExtents(v);
      }.bind(this));
      this.ops.push({
        op: "region",
        value: ar,
        label: label,
        color: color,
      });
    }

    axes() {
      this.ops.push({
        op: "axes",
      });
    }

    _updateExtents(v) {
      if (v[1] > this.extent.xmax) {
        this.extent.xmax = v[1];
      }
      if (v[1] < this.extent.xmin) {
        this.extent.xmin = v[1];
      }
      if (v[2] > this.extent.ymax) {
        this.extent.ymax = v[2];
      }
      if (v[2] < this.extent.ymin) {
        this.extent.ymin = v[2];
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
      var y_css_extent = this.canvas.height;
      var x_css_extent = this.canvas.width;
      var x_source_extent = 1.5 * (this.extent.xmax - this.extent.xmin);
      var y_source_extent = 1.5 * (this.extent.ymax - this.extent.ymin);
      var source_extent = Math.max(x_source_extent, y_source_extent);
      var x_origin = -this.extent.xmin + 0.25 * source_extent;
      var y_origin =  this.extent.ymax + 0.25 * source_extent;
      var x_ratio = (x_css_extent/source_extent);
      var y_ratio = (y_css_extent/source_extent);
      var rotPi = [-1, 0, 0, 0];
      var mid = [0.5, 0, 0, 0];
      var xform = function(v) {
        return [(v[1]+x_origin)*x_ratio, (-v[2]+y_origin)*y_ratio];
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
          var textLoc = g.add(op.offset, op.value);
          var nativeTextLoc = xform(textLoc);
          nativeTextLoc[0] += 9;
          nativeTextLoc[1] -= 9;
          this._text(nativeTextLoc, op.label)
        } else if (op.op == "axes") {
          this.ctx.beginPath();
          this.ctx.strokeStyle = "#ddd";
          this.ctx.moveTo(0, y_origin*y_ratio);
          this.ctx.lineTo(x_css_extent, y_origin*y_ratio);
          this.ctx.moveTo(x_origin*x_ratio, 0);
          this.ctx.lineTo(x_origin*x_ratio, y_css_extent);
          this.ctx.stroke();
        } else if (op.op == "region") {
          this.ctx.beginPath();
          if (op.color) {
            this.ctx.fillStyle = op.color;
          } else {
            this.ctx.fillStyle = "rgba(90, 0, 255, 0.5)";
          }
          this._moveto(xform(op.value[0]));
          op.value.forEach(function(v) {
            this._lineto(xform(v));
          }.bind(this));
          this.ctx.fill();
        }
      }.bind(this));
    }
  }

  d.Frame = Frame;

  return d;
}();
