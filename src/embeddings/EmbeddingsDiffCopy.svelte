<script>
    // export let embeddingsOrig;
    import nj, { max } from 'numjs';
    import heatmap from 'simpleheat';
    import { onMount } from 'svelte';
    let ch=400, cw=400;
    let canvas, d, hm, edh=100, edw=50, hmMax=100, hmRad=1, hmBlur=1;
    let canvas2;
    $: {
        d = nj.zeros([3, edh, edw]);
        for(let i=0; i<edh; i++) {
            for(let j=0; j<edw; j++) {
                d.set(0,i,j,j);
                d.set(1,i,j,i);
                d.set(2,i,j,getRand(i,j));
            }
        }
        d = d.transpose(1,2,0);
        d = d.reshape(edh*edw, 3);
        console.log(d.shape, d.slice([0,3]).tolist(), d);
    }

    function getRand(i,j) {
        return i;
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
        handleHeatmapChange();

        canvas2.height = ch;
        canvas2.width = cw;
        paintInCanvas(canvas2, d);
    })

    function paintInCanvas(c, numjsArray) {
        let ctx = c.getContext('2d');
        let imgData = ctx.getImageData(0, 0, cw, ch);
        let [nh, nw] = numjsArray.shape;
        for(let i=0; i<imgData.data.length; i+=4) {
            let h = parseInt(i/(4*cw));
            let w = (i/4) % ch;
            let r = 0, g = 0, b = 0;
            if(h<nh && w<nw) 
                r = Math.min((numjsArray.get(h,w) / hmMax)*255, 255);
            imgData.data[i + 0] = r;
            imgData.data[i + 1] = g;
            imgData.data[i + 2] = b;
            imgData.data[i + 3] = 255;
        }
        ctx.putImageData(imgData, 0, 0);
    }

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
    <canvas bind:this={canvas2} />
</div>
