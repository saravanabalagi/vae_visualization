<script>
    export let embeddingsOrig;
    import nj from 'numjs';
    import heatmap from 'simpleheat';
    import { onMount } from 'svelte';
    import { Button, Switch } from 'svelma';

    let embeddings, embeddingsDiff;
    let canvas, d, hm, edh, edw;
    let hmMax=10, hmRad=1, hmBlur=1;
    let diffFromFirst = false;
    $: {
        embeddings = nj.array(embeddingsOrig);
        let view1;
        if (diffFromFirst) 
            view1 = nj.stack(Array.from(Array(embeddings.shape[0]-1)).map(e => embeddings.pick(0)));
        else view1 = embeddings.slice([null,-1]);
        let view2 = embeddings.slice(1);
        embeddingsDiff = nj.abs(view1.subtract(view2));
        [edh, edw] = embeddingsDiff.shape;
        d = nj.zeros([3, edh, edw]);
        for(let i=0; i<edw; i++) {
            for(let j=0; j<edh; j++) {
                d.set(0,j,i,i);
                d.set(1,j,i,j);
                d.set(2,j,i,embeddingsDiff.get(i,j));
            }
        }
        d = d.transpose(1,2,0);
        d = d.reshape(edh*edw, 3);
        // console.log(d.shape, d.slice([0,3]).tolist(), d);
        if(hm != null) handleHeatmapChange();
    }

    onMount(() => {
        canvas.height = edh;
        canvas.width = edw;
        console.debug('component loaded', canvas, d);
        hm = heatmap(canvas);
        handleHeatmapChange();
    })

    function handleHeatmapChange() {
        hm.data(d.tolist());
        hm.radius(hmRad, hmBlur);
        hm.max(hmMax);
        hm.draw();
    }

    function getCsvContent(numjsArray) {
        if(numjsArray.shape.length !== 2)
            console.error(`Can only get 2D csv, got shape ${numjsArray.shape}`);
        let csvContent = numjsArray.tolist().map(e => e.join(",")).join("\n");
        return `data:text/csv;charset=utf-8,${csvContent}`;
    }

    function downloadCsv(csvContent) {
        let encodedUri = encodeURI(csvContent);
        let link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "results.csv");
        document.body.appendChild(link); // Required for FF
        link.click();
        document.body.removeChild(link); 
    }

    // const [height, width] = embeddingsDiff.shape;
    // let canvas = document.createElement('canvas');
    // let ctx = canvas.getContext('2d');
    // let imgData = ctx.createImageData(width, height);
    // imgData.data.set(buffer);
    // ctx.putImageData(imgData, 0, 0);
    // let dataUri = canvas.toDataURL();
    // image.src = dataUri;

</script>

<div class="embeddingDiff">
    <div class="canvasWrapper">
        <canvas bind:this={canvas} />
    </div>
    <div class="canvasControls ml-4">
        <div class="field">
            <Switch bind:checked={diffFromFirst} type="is-primary">First</Switch>
        </div>
        <div class="inputControls mt-2">
            <input type="number" bind:value={hmMax} min=0 max=100 step=0.01 on:change={handleHeatmapChange} />
            <input class="ml-2" type="number" bind:value={hmRad} min=0 max=100 step=0.01 on:change={handleHeatmapChange} />
            <input class="ml-2" type="number" bind:value={hmBlur} min=0 max=100 step=0.01 on:change={handleHeatmapChange} />
        </div>
        <div class="buttonControls mt-3">
            <Button type="is-info" on:click={() => {downloadCsv(getCsvContent(embeddings))}}>Embeddings CSV</Button>
            <Button class="ml-2" type="is-info" on:click={() => {downloadCsv(getCsvContent(embeddingsDiff))}}>EmbeddingsDiff CSV</Button>
        </div>
    </div>
</div>

<style lang="scss">
.embeddingDiff, .inputControls, .buttonControls {
    display: flex;
    flex-direction: row;
}
.inputControls input {
    width: auto;
}
.canvasControls {
    display: flex;
    flex-direction: column;
}
.canvasWrapper {
    height: 500px;
    overflow-y: auto;
    -ms-overflow-style: none;  /* Internet Explorer 10+ */
    scrollbar-width: none;  /* Firefox */
    &::-webkit-scrollbar { 
        display: none;  /* Safari and Chrome */
    }
}
</style>
