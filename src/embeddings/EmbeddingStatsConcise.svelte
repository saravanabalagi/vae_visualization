<script>
import {Tag} from 'svelma';
import DiffValue from './DiffValue.svelte';

export let diff = false;
export let name;
export let mu;
export let sigma;
export let l1;
</script>

<div class="stats flex-row">
    <div>
        {#if name}
            <Tag type="is-warning">{name}</Tag>
        {:else}
            <div class="px-5" />
        {/if}
    </div>
    <div class="flex-row">
        <div class="mx-1 has-text-grey-light">µ</div>
        <DiffValue classes="mx-1" value={mu} {diff} />
    </div>
    <div class="flex-row">
        <div class="mx-1 has-text-grey-light">σ</div>
        <DiffValue classes="mx-1" value={sigma} {diff} />
    </div>
    <div class="flex-row">
        <div class="mx-1 has-text-grey-light">L1</div>
        <DiffValue classes="mx-1" value={l1} {diff} />
    </div>
</div>

<style lang="scss">
.stats {
    justify-content: space-between;
}
.diff.green { color: green; }
.diff.red { color: red; }
</style>
