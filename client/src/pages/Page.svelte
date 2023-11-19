<script>
    import HttpController from "../components/HttpController.svelte";
    import NotificationsController from "../components/NotificationsController.svelte";
    import Footer from "../components/Footer.svelte";
    import NavBar from "../components/NavBar.svelte";
</script>

<HttpController>
    <NotificationsController>
        <NavBar page={window.page_title} internal_login_enabled={window.internal_login_enabled} name={window.user_name} profile_pic={window.profile_pic} />

        <div class="px-4 lg:px-[15%] page-height">
            <slot></slot>
        </div>

        <Footer />
    </NotificationsController>
</HttpController>

<style>
    .page-height {
        min-height: calc(100vh - 10rem);
    }
</style>
