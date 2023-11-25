<script lang="ts">
    export let text: string;

    interface IFragment {
        is_link: boolean;
        is_line_break: boolean;
        text: string;
    }

    let fragments: IFragment[] = [];

    $: update_fragments(text);

    function update_fragments(text: string) {
        fragments = [];

        let current_fragment: IFragment = {
            is_link: false,
            is_line_break: false,
            text: ""
        };

        function push_fragment({ is_line_break, with_ch }: { is_line_break?: boolean, with_ch?: string }) {
            fragments.push(current_fragment);
            current_fragment = {
                is_link: false,
                is_line_break: is_line_break ?? false,
                text: with_ch ?? ""
            };
        }

        function is_link(str: string) {
            return str.startsWith("http://") || str.startsWith("https://") || str.startsWith("www.");
        }

        for (const ch of [...text]) {
            if (ch === " ") {
                push_fragment({ with_ch: ch });
                push_fragment({});
                continue;
            } else if (ch === "\n") {
                push_fragment({ is_line_break: true });
                push_fragment({});
                continue;
            } else {
                current_fragment.text += ch;
                if (is_link(current_fragment.text)) {
                    current_fragment.is_link = true;
                }
                continue;
            }
        }

        fragments.push(current_fragment);

        fragments = fragments;
    }
</script>

{#each fragments as fragment}
    {#if fragment.is_link}
        <a class="text-purple-600 dark:text-purple-300 hover:underline" href="{fragment.text}" target="_blank" style="overflow-wrap: anywhere">{fragment.text}</a>
    {:else if fragment.is_line_break}
        <br />
    {:else}
        {fragment.text}
    {/if}
{/each}
