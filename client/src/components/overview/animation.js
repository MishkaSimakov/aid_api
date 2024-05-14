import {Scene} from "@/components/overview/Scene";

export const animate = (canvasId, tickers, indices, router) => {
    const scene = new Scene(canvasId);

    if (!scene.isSupported()) {
        alert('Your browser does not support canvas. Content wont be displayed.');
        return;
    }

    scene.addEventListeners();
    scene.addTickers(tickers);
    scene.setIndices(indices);
    scene.setRouter(router);

    scene.startAnimation();

    return scene;
};
