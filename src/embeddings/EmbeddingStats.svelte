<script>
import { getMean, getStd, getLNorm } from '../utils';
import InfoTable from './InfoTable.svelte';

export let embedding;
export let embeddingPrev;
let info, infoHeader, diff;
$: {
    const embeddingMean = getMean(embedding);
    const embeddingStd = getStd(embedding);
    const embeddingL0 = getLNorm(embedding, 0);
    const embeddingL1 = getLNorm(embedding, 1);
    const embeddingL2 = getLNorm(embedding, 2);
    const embeddingLInf = getLNorm(embedding, Infinity);

    if (embeddingPrev.length === 0) {
        diff = [false, false];
        infoHeader = ['Stats', 'Embedding'];
        info = {
            'µ': [embeddingMean],
            'σ': [embeddingStd],
            'L0': [embeddingL0],
            'L1': [embeddingL1],
            'L2': [embeddingL2],
            'LInf': [embeddingLInf],
        }
    } else {
        const delta = embedding.map((v, i) => v-embeddingPrev[i]);

        const deltaMean = getMean(delta);
        const deltaStd = getStd(delta);
        const deltaL0 = getLNorm(delta, 0);
        const deltaL1 = getLNorm(delta, 1);
        const deltaL2 = getLNorm(delta, 2);
        const deltaLInf = getLNorm(delta, Infinity);

        const meanDelta = getMean(embedding) - getMean(embeddingPrev);
        const stdDelta = getStd(embedding) - getStd(embeddingPrev);
        const l0Delta = getLNorm(embedding, 0) - getLNorm(embeddingPrev, 0);
        const l1Delta = getLNorm(embedding, 1) - getLNorm(embeddingPrev, 1);
        const l2Delta = getLNorm(embedding, 2) - getLNorm(embeddingPrev, 2);
        const lInfDelta = getLNorm(embedding, Infinity) - getLNorm(embeddingPrev, Infinity);

        infoHeader = ['Stats', 'Embedding', 'Change', 'Delta']
        diff = [false, false, true, false];
        info = {
            'µ': [embeddingMean, meanDelta, deltaMean],
            'σ': [embeddingStd, stdDelta, deltaStd],
            'L0': [embeddingL0, l0Delta, deltaL0],
            'L1': [embeddingL1, l1Delta, deltaL1],
            'L2': [embeddingL2, l2Delta, deltaL2],
            'LInf': [embeddingLInf, lInfDelta, deltaLInf],
        }
    }
}
</script>

<InfoTable info={info} header={infoHeader} diff={diff} />

