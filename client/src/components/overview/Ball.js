const Vector = require('vector2js');

// some physics stuff was borrowed from here:
// https://github.com/markhobson/balls-js/blob/master/Ball.js

export const Ball = class {
    position;
    velocity = new Vector(0, 0);
    radius;
    title;
    is_category_name;
    gravitates_to = undefined;

    isMovable() {
        return !this.is_category_name;
    }

    makeTimeStep(dt) {
        this.position.addSelf(this.velocity.mulScalar(dt));
    }

    resolveCollision(other, damping) {
        if (damping > 1) {
            return;
        }

        let hasIntersection = this.position.distanceFrom(other.position) < this.radius + other.radius;

        // balls are not intersecting
        if (!hasIntersection) {
            return;
        }

        let tangentAxis = other.position.sub(this.position).normalize();
        let normalAxis = new Vector(-tangentAxis.y, tangentAxis.x);

        let tangentRelativeSpeed = this.velocity.sub(other.velocity).dot(tangentAxis);

        // balls move away from each other
        if (tangentRelativeSpeed <= 0) {
            return;
        }

        [this, other].forEach(ball => {
            if (ball.isMovable()) {
                let tangentProjection = ball.velocity.dot(tangentAxis);
                if (Math.abs(tangentProjection) < 0.05) {
                    tangentProjection = Math.sign(tangentProjection) * 0.05;
                }

                tangentProjection /= 2;

                let normalProjection = ball.velocity.dot(normalAxis);

                ball.velocity = normalAxis.mulScalar(normalProjection)
                    .sub(tangentAxis.mulScalar(tangentProjection));

                ball.velocity.mulScalarSelf(1 - damping);
            }
        });
    }

    contains(position) {
        return this.position.distanceFrom(position) <= this.radius;
    }
};
