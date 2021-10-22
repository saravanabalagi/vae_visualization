<script>
import { onMount } from 'svelte';

export let embedding = [];
export let width;
export let maxValue; 
let canvas;

const draw = () => {
    if (canvas == null) return;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.beginPath();
    const widthHalf = width / 2;
    for (let i=0; i<embedding.length; i++) {
        const offset =  widthHalf * embedding[i] / maxValue;
        let startOffset, endOffset;
        if (embedding[i] > 0) {
            startOffset = 0
            endOffset = offset;
        } else {
            startOffset = offset;
            endOffset = 0;
        }
        ctx.strokeStyle = "#238cd1";
        ctx.moveTo(widthHalf + startOffset, i);
        ctx.lineTo(widthHalf + endOffset, i);
        ctx.stroke();
    }
}

onMount(draw);
$: embedding, draw();

</script>

<canvas
    bind:this={canvas}
    {width}
    height={embedding.length}
    >
</canvas>
