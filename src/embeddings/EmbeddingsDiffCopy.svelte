<script>
    // export let embeddingsOrig;
    import nj from 'numjs';
    import heatmap from 'simpleheat';
    import { onMount } from 'svelte';
    import {data as datac} from './data';

    let ch=1205, cw=15;
    let canvas, d, hm, edh=1205, edw=15, hmMax=10, hmRad=1, hmBlur=1;
    $: {
        d = nj.zeros([3, edh, edw]);
        for(let i=0; i<edw; i++) {
            for(let j=0; j<edh; j++) {
                d.set(0,j,i,i);
                d.set(1,j,i,j);
                d.set(2,j,i,Math.random()*10);
            }
        }
        d = d.transpose(1,2,0);
        d = d.reshape(edh*edw, 3);
        console.log(d.shape, d.slice([0,3]).tolist(), d);
    }

    function handleHeatmapChange() {
        hm.radius(hmRad, hmBlur);
        hm.max(hmMax);
        hm.draw();
    }

    function handleCanvasChange() {
        canvas.height = ch;
        canvas.width = cw;
        hm.resize();
        hm.draw();
    }

    onMount(() => {
        canvas.height = ch;
        canvas.width = cw;
        // console.log('component loaded', canvas, d);
        hm = heatmap(canvas).data(d.tolist())
        hm.radius(1,1);
        hm.max(hmMax);
        hm.draw();
    })

</script>

<div>
    <div>
        <input type="number" bind:value={hmMax} min=1 max=100 step=1 on:change={handleHeatmapChange} />
        <input type="number" bind:value={hmRad} min=1 max=100 step=0.01 on:change={handleHeatmapChange} />
        <input type="number" bind:value={hmBlur} min=1 max=100 step=0.01 on:change={handleHeatmapChange} />
        <input type="number" bind:value={ch} min=1 max=1500 step=1 on:change={handleCanvasChange} />
        <input type="number" bind:value={cw} min=1 max=1500 step=1 on:change={handleCanvasChange} />
    </div>
    <canvas bind:this={canvas} />
</div>
