<script lang="ts">
    export let text: string;

    interface IFragment {
        is_link: boolean;
        is_line_break: boolean;
        text: string;
    }

    let fragments: IFragment[] = [];

    $: {
        function is_link(str: string) {
            return str.startsWith("http://") || str.startsWith("https://") || str.startsWith("www.");
        }

        fragments = text?.trim().split(" ").reduce((frags, text, i) => {
            const line_breaks = text.split("\n");

            if (line_breaks.length > 1) {
                for (const br of line_breaks) {
                    if (br.length > 0) {
                        frags.push({
                            text: br
                        });
                    }

                    frags.push({
                        is_line_break: true
                    });
                }

                return frags;
            }

            frags.push({
                is_link: is_link(text),
                text: `${i > 0 ? " " : ""}${text}`
            });

            return frags;
        }, []);
    }
</script>

{#each fragments as fragment}
    {#if fragment.is_link}
        <a class="text-purple-600 hover:underline" href="{fragment.text}" target="_blank" style="overflow-wrap: anywhere">{fragment.text}</a>
    {:else if fragment.is_line_break}
        <br />
    {:else}
        {fragment.text}
    {/if}
{/each}
