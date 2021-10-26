<script>
import {isObj} from '../utils';
import DiffValue from './DiffValue.svelte';

export let header = null;
export let info = {};
export let diff = false;
export let precision = 2;
</script>

<table class="table is-striped info-table">
    {#if header}
        <tr class="row header-row">
            {#each header as v}
                <th class="header">{v}</th>
            {/each}
        </tr>
    {/if}
    <tbody>
        {#each Object.entries(info) as [k, v]}
            <tr class="row">
                <td class="key">{k}</td>
                {#if Array.isArray(v)}
                    {#each v as e, i}
                        <td class="value">
                            <DiffValue value={e} diff={(diff[i+1] != null) ? diff[i+1] : diff} {precision} />
                        </td>
                    {/each}
                {:else if isObj(v)}
                    <svelte:self info={v} />
                {:else}
                    <td class="value">
                        <DiffValue classes="mx-1" value={v} {diff} {precision} />
                    </td>
                {/if}
            </tr>
        {/each}
    </tbody>
</table>

<style lang="scss">
.info-table {
    margin: 10px 0;
    tr > th:not(:first-child) { text-align: right; }
    .row {
        td, th { padding: 0; }
        transition: all 1300ms ease-in-out;
        &:hover {
            transition: all 300ms ease-in-out;
            background-color: #EEE;
        }
        .key {
            color: #999;
        }
        .value {
            text-align: right;
        }
    }
}
</style>
