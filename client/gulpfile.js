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
    return exec("npm run build", processCallback);
}

function copyGlobalStyles() {
    return src("./src/*.less")
        .pipe(less())
        .pipe(dest("./public/gulp_build"));
}

const buildOnly = series(copyGlobalStyles, validateTs, build);

function buildProject() {
    watch(["./src/**/*", "!./src/**/*.spec.ts"], { ignoreInitial: false }, series(copyGlobalStyles, validateTs, build));
}

const _default = buildProject;
export { _default as default };
export { buildOnly }
