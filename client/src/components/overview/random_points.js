const Vector = require("vector2js");

export const generateSpacedRandomPositions = (count, minDistance, maxDistance) => {
    const attemptsPerPoint = 200;
    let generatedPoints = [];
    let newPoints = [];

    newPoints.push(new Vector(0, 0));

    while (newPoints.length + generatedPoints.length !== count) {
        if (newPoints.length === 0) {
            newPoints.push(...generatedPoints);
            generatedPoints = [];
        }

        let randomIndex = Math.floor(Math.random() * (newPoints.length - 0.001));
        let sourcePoint = newPoints[randomIndex];

        for (let attempt = 0; attempt < attemptsPerPoint; ++attempt) {
            let randomAngle = Math.random() * Math.PI * 2;
            let randomDistance = minDistance + Math.random() * (maxDistance - minDistance);

            let position = sourcePoint.add((new Vector(1, 0))
                .rotateRadians(randomAngle).mulScalar(randomDistance));

            let foundTooClose = false;
            let foundCloseEnough = false;
            [...generatedPoints, ...newPoints].every(point => {
                let distance = point.distanceFrom(position);

                if (distance < minDistance) {
                    foundTooClose = true;
                    return false;
                }

                if (distance < maxDistance) {
                    foundCloseEnough = true;
                }

                return true;
            });

            if (foundTooClose || !foundCloseEnough) {
                continue;
            }

            newPoints.push(position);

            if (newPoints.length + generatedPoints.length === count) {
                break;
            }
        }

        generatedPoints.push(sourcePoint);
        newPoints.splice(randomIndex, 1);
    }

    generatedPoints.push(...newPoints);

    return generatedPoints;
};
