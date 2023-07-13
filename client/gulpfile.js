const { src, dest, series, watch } = require("gulp");
const less = require("gulp-less");
const { exec } = require("child_process");

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
        .pipe(dest("./public/build"));
}

function buildProject() {
    watch("./src/**/*", { ignoreInitial: false }, series(copyGlobalStyles, validateTs, build));
}

exports.default = series(copyLibraryContent, buildProject);
