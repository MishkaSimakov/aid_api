import {generateSpacedRandomPositions} from "@/components/overview/random_points";

const Vector = require('vector2js');

import {Ball} from "@/components/overview/Ball";
import {PanAndZoom} from "@/components/overview/PanAndZoom";
import {World} from "@/components/overview/World";

export const Scene = class {
    world;
    context;
    canvas;
    panAndZoomHandler;

    indexBallColor = '#118ab2';
    indicesPositions = {};

    hoveredBallIndex = -1;
    indexTooltip = undefined;

    indices = {};
    router = undefined;

    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.context = this.canvas.getContext("2d");

        this.resizeCanvas();

        this.world = new World();
    }

    // isFirstTime() {
    //     return localStorage.getItem("financial.visited") === null;
    // }
    //
    // setVisited() {
    //     localStorage.setItem("financial.visited", "true");
    // }

    addTickers(tickers) {
        let indices = Object.keys(tickers);

        let randomPositions = generateSpacedRandomPositions(indices.length, 2500, 15000);

        indices.forEach(index => {
            this.indicesPositions[index] = randomPositions.pop();
        });

        let indicesTickersPositions = {};
        indices.forEach(index => {
            indicesTickersPositions[index] = generateSpacedRandomPositions(
                tickers[index].length + 1, 250, 500
            );
        });

        this.world.balls.push(...indices.map(index => {
            let index_ball = new Ball();
            index_ball.position = this.indicesPositions[index];
            index_ball.radius = 75;
            index_ball.is_category_name = true;
            index_ball.title = index;

            this.world.balls.push(...tickers[index].map(ticker => {
                let ticker_ball = new Ball();

                ticker_ball.position = index_ball.position
                    .add(indicesTickersPositions[index].pop());
                ticker_ball.radius = 50 + ticker.weight * 2;
                ticker_ball.is_category_name = false;
                ticker_ball.title = ticker.name;
                ticker_ball.gravitates_to = index_ball;

                return ticker_ball;
            }));

            return index_ball;
        }));
    }

    setIndices(indices) {
        indices.forEach(index => {
            this.indices[index.id] = index.name;
        });
    }

    setRouter(router) {
        this.router = router;
    }

    addEventListeners() {
        this.panAndZoomHandler = new PanAndZoom(this.canvas);
        this.panAndZoomHandler.transform.translate(
            new Vector(this.canvas.width / 2, this.canvas.height / 2)
        );
        this.panAndZoomHandler.onChange = () => {
            this.router.replace({query: {}});
        };

        this.canvas.addEventListener('mousemove', e => this.updateHoveredBall(e));
        this.canvas.addEventListener('mousedown', e => this.navigateToTickerPage(e));
        window.addEventListener('resize', () => this.resizeCanvas());
    }

    navigateToTickerPage() {
        if (this.hoveredBallIndex === -1) {
            return;
        }

        if (this.world.balls[this.hoveredBallIndex].is_category_name) {
            return;
        }

        if (this.router === undefined) {
            return;
        }

        this.panAndZoomHandler.resetDrag();
        let ticker = this.world.balls[this.hoveredBallIndex].title;
        this.router.push({path: `/tickers/${ticker}`});
    }

    updateHoveredBall(evt) {
        evt.preventDefault();
        evt.stopPropagation();

        let position = this.panAndZoomHandler.transform
            .transform(this.panAndZoomHandler.mouseOffset(evt));
        let positionVector = new Vector(position.x, position.y);

        this.hoveredBallIndex = this.world.balls.findIndex(ball => ball.contains(positionVector));

        if (this.hoveredBallIndex !== -1 && this.world.balls[this.hoveredBallIndex].is_category_name) {
            this.showIndexTooltip(evt.pageX, evt.pageY);
        } else if (this.indexTooltip !== undefined) {
            this.indexTooltip.remove();
            this.indexTooltip = undefined;
        }
    }

    showIndexTooltip(mouseX, mouseY) {
        if (this.indexTooltip !== undefined) {
            this.indexTooltip.style.left = `${mouseX}px`;
            this.indexTooltip.style.top = `${mouseY}px`;
            return;
        }

        let index = this.world.balls[this.hoveredBallIndex].title;

        const container = document.createElement("div");
        container.style.position = "absolute";
        container.style.left = `${mouseX}px`;
        container.style.top = `${mouseY}px`;
        container.style.pointerEvents = "none";

        container.classList.add("border", "rounded", "bg-light", "p-3")

        const tooltipText = document.createElement("p");
        tooltipText.classList.add("m-0");
        tooltipText.innerHTML = this.indices[index];

        container.appendChild(tooltipText);

        this.indexTooltip = document.body.appendChild(container);
    }

    getBallColor(ball) {
        if (ball.is_category_name) {
            return this.indexBallColor;
        }

        if (this.hoveredBallIndex !== -1 && ball === this.world.balls[this.hoveredBallIndex]) {
            return '#07FCBA';
        }

        return '#06d6a0';
    }

    drawTickerBall(ball) {
        let position = ball.position;

        this.context.beginPath();
        this.context.arc(position.x, position.y, ball.radius, 0, 2 * Math.PI, false);
        this.context.fillStyle = this.getBallColor(ball);
        this.context.fill();

        this.context.fillStyle = 'white';
        this.context.font = '20px arial';
        this.context.textAlign = 'center';
        this.context.textBaseline = 'middle';
        this.context.fillText(ball.title, position.x, position.y);
    }

    drawBalls() {
        this.panAndZoomHandler.clearCanvas();

        this.world.balls.forEach(ball => {
            this.drawTickerBall(ball);
        });
    }

    resizeCanvas() {
        let transform = this.context.getTransform();

        let width = this.canvas.clientWidth;
        let height = this.canvas.clientHeight;

        this.canvas.width = width;
        this.canvas.height = height;

        this.context.setTransform(transform);
    }

    isSupported() {
        return !!this.context;
    }

    makeAnimationStep(dt) {
        this.world.makeTimeStep(dt)
        this.drawBalls();
    }

    startAnimation() {
        let prev_frame_time = Date.now();

        const animationLoop = () => {
            let current_time = Date.now();
            let delta = current_time - prev_frame_time;

            this.world.damping += delta / 1000 / 100;

            this.makeAnimationStep(Math.min(delta, 100));

            prev_frame_time = current_time;

            window.requestAnimationFrame(animationLoop);
        }

        window.requestAnimationFrame(animationLoop);
    }

    transitionTo(index, duration) {
        if (this.indicesPositions[index] === undefined) {
            return;
        }

        function easeInOutSine(x) {
            return -(Math.cos(Math.PI * x) - 1) / 2;
        }

        // we should move center of screen to given index position
        let zero_position = this.panAndZoomHandler.transform.transform(new Vector(0, 0));
        let center_position = this.panAndZoomHandler.transform.transform(new Vector(this.canvas.width / 2, this.canvas.height / 2));
        let screen_center_offset = center_position.sub(zero_position);

        let startPosition = zero_position;
        let endPosition = this.indicesPositions[index].sub(screen_center_offset);

        if (duration === 0) {
            this.panAndZoomHandler.transform.setOffset(endPosition);
            return;
        }

        let startTime = Date.now();

        let animation = () => {
            let currentTime = Date.now();
            let timeProgress = (currentTime - startTime) / duration;

            if (timeProgress > 1) {
                this.panAndZoomHandler.transform.setOffset(endPosition);
                this.panAndZoomHandler.unlock();

                return;
            }

            let progress = easeInOutSine(timeProgress);

            let newPosition = startPosition.mulScalar(1 - progress)
                .add(endPosition.mulScalar(progress));

            this.panAndZoomHandler.transform.setOffset(newPosition);

            window.requestAnimationFrame(animation);
        };

        this.panAndZoomHandler.lock();
        window.requestAnimationFrame(animation);
    }
};
