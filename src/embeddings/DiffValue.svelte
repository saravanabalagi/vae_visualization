<script>
export let diff = false;
export let value;
export let classes;
export let precision = 2;
</script>

<div
    class="{classes}"
    class:diff={diff}
    class:green={value > 0}
    class:red={value < 0}
    >
    {#if !Number.isNaN(value) && !Number.isInteger(value)}
        {value.toFixed(precision)}
    {:else}
        {value}
    {/if}
</div>

<style lang="scss">
.diff.green { color: green; }
.diff.red { color: red; }
</style>
