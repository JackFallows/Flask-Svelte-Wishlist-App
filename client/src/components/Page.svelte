<script>
    import HttpController from "./HttpController.svelte";
    import Footer from "./Footer.svelte";
    import NavBar from "./NavBar.svelte";
</script>

<HttpController>
    <NavBar page={window.page_title} internal_login_enabled={window.internal_login_enabled} name={window.user_name} profile_pic={window.profile_pic} />

    <div class="px-4 lg:px-[15%] page-height">
        <slot></slot>
    </div>

    <Footer />
</HttpController>

<style>
    .page-height {
        min-height: calc(100vh - 14rem);
    }
</style>
