const Vector = require('vector2js');

// taken from here:
// https://gist.github.com/balazsbotond/1a876d8ccec87e961ec4a4ae5efb5d33

class Transform {
    constructor(ctx) {
        this.ctx = ctx;
        this.s = 1;
        this.dx = 0;
        this.dy = 0;
    }

    scale(s) {
        this.ctx.scale(s, s);
        this.s *= 1 / s;
        this.dx *= 1 / s;
        this.dy *= 1 / s;
    }

    setOffset(position) {
        this.ctx.translate(this.dx - position.x, this.dy - position.y);
        this.dx = position.x;
        this.dy = position.y;
    }

    translate(delta) {
        this.ctx.translate(delta.x, delta.y);
        this.dx -= delta.x;
        this.dy -= delta.y;
    }

    transform(position) {
        return new Vector(
            this.s * position.x + this.dx,
            this.s * position.y + this.dy
        );
    }

    inverse(position) {
        return new Vector(
            (position.x - this.dx) / this.s,
            (position.y - this.dy) / this.s
        )
    }
}

export const PanAndZoom = class {
    isLocked = false;
    onChange = undefined;

    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = this.canvas.getContext('2d');
        this.transform = new Transform(this.ctx);

        this.canvas.addEventListener('wheel', e => this.onWheel(e));
        this.canvas.addEventListener('mousedown', e => this.onMouseDown(e));
        this.canvas.addEventListener('mousemove', e => this.onMouseMove(e));
        this.canvas.addEventListener('mouseup', e => this.onMouseUp(e));
    }

    lock() {
        this.isLocked = true;
    }

    unlock() {
        this.isLocked = false;
    }

    resetDrag() {
        this.dragging = false;
    }

    mouseOffset(e) {
        return new Vector(
            e.pageX - this.canvas.offsetLeft,
            e.pageY - this.canvas.offsetTop
        );
    }

    onMouseDown(e) {
        e.preventDefault();
        e.stopPropagation();

        if (this.isLocked) {
            return;
        }

        this.dragStart = this.transform.transform(this.mouseOffset(e));
        this.dragging = true;
    }

    onMouseMove(e) {
        e.preventDefault();
        e.stopPropagation();

        if (this.isLocked) {
            return;
        }

        if (!this.dragging) {
            return;
        }

        const offset = this.mouseOffset(e);
        const dragEnd = this.transform.transform(offset);
        const delta = dragEnd.sub(this.dragStart);

        this.transform.translate(delta);
        this.dragStart = this.transform.transform(offset);

        this.onChange?.();
    }

    onMouseUp(e) {
        e.preventDefault();
        e.stopPropagation();

        if (this.isLocked) {
            return;
        }

        this.dragging = false;
    }

    onWheel(e) {
        e.preventDefault();
        e.stopPropagation();

        if (this.isLocked) {
            return;
        }

        let offset = this.mouseOffset(e);
        let zoomCenter = this.transform.transform(offset);
        let factor = Math.sign(e.deltaY) > 0 ? 0.9 : 1.1;

        this.transform.translate(zoomCenter);
        this.transform.scale(factor);
        this.transform.translate(zoomCenter.invert());

        this.onChange?.();
    }

    clearCanvas() {
        const leftTop = this.transform.transform(new Vector(0, 0));
        const rightBottom = this.transform.transform(new Vector(
            this.ctx.canvas.width,
            this.ctx.canvas.height
        ));

        const width = Math.abs(rightBottom.x - leftTop.x);
        const height = Math.abs(rightBottom.y - leftTop.y);
        this.ctx.clearRect(leftTop.x, leftTop.y, width, height);
    }
}
