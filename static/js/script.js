const jdFile = document.getElementById("jdFile");
const resumeFile = document.getElementById("resumeFile");

const jdName = document.getElementById("jdName");
const resumeName = document.getElementById("resumeName");


jdFile.addEventListener("change", () => {

    if (jdFile.files.length) {

        jdName.textContent = jdFile.files[0].name;

    }

});

resumeFile.addEventListener("change", () => {

    if (resumeFile.files.length) {

        resumeName.textContent = resumeFile.files[0].name;

    }

});
