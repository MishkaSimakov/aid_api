export const World = class {
    balls = [];
    damping = 0;

    makeTimeStep(dt) {
        if (this.damping > 1) {
            return;
        }

        this.balls.forEach(ball => {
            if (ball.is_category_name) {
                return;
            }
            if (ball.gravitates_to === undefined) {
                return;
            }

            let gravity_center = ball.gravitates_to.position;
            let mass = ball.radius * ball.radius;

            let distance = ball.position.distanceFrom(gravity_center);

            let force = (1 - this.damping) * mass * (1 / (distance * distance));

            let direction = gravity_center.sub(ball.position).normalize();

            let acceleration = direction.mulScalar(force / mass * dt);
            ball.velocity.addSelf(acceleration);
        });

        this.balls.forEach(ball => {
            ball.makeTimeStep(dt);
        });

        for (let i = 0; i < this.balls.length; ++i) {
            for (let j = i + 1; j < this.balls.length; ++j) {
                this.balls[i].resolveCollision(this.balls[j], this.damping);
            }
        }
    }
};
