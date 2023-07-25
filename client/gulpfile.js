import gulp from "gulp";
import less from "gulp-less";
import { exec } from "child_process";

const { src, dest, series, watch } = gulp;


function processCallback(error, stdout, stderr) {
    if (error) {
        console.error(`exec error: ${error}`);
    }

    if (stdout) {
        console.log(`stdout: ${stdout}`);
    }

    if (stderr) {
        console.error(`stderr: ${stderr}`);
    }
}

function validateTs() {
    return exec("npm run validate", processCallback)
}

function build() {
    return exec("npm run build-debug", processCallback);
}

function copyLibraryContent() {
    return src([
        "./node_modules/bootstrap/dist/css/bootstrap.min.css",
        "./node_modules/bootstrap/dist/js/bootstrap.min.js",
        "./node_modules/@popperjs/core/dist/umd/popper.min.js"
    ])
    .pipe(dest("./public/library_content"));
}

function copyGlobalStyles() {
    return src("./src/*.less")
        .pipe(less())
        .pipe(dest("./public/gulp_build"));
}

function buildProject() {
    watch(["./src/**/*", "!./src/**/*.spec.ts"], { ignoreInitial: false }, series(copyGlobalStyles, validateTs, build));
}

const _default = series(copyLibraryContent, buildProject);
export { _default as default };
