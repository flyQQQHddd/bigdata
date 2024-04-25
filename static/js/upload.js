const form = document.querySelector("form");
const fileInput = document.querySelector(".file-input");
const progressArea = document.querySelector(".progress-area");
const uploadedArea = document.querySelector(".uploaded-area");

let filesToUpload = []; // 存储要上传的文件队列
let currentUpload = null; // 当前上传的文件
let isLastFile = false; // 标记是否是最后一个文件

// form click event
form.addEventListener("click", () => {
  fileInput.click();
});

fileInput.onchange = ({ target }) => {
  const files = target.files;
  if (files.length === 0) return;

  // 将所有文件添加到上传队列
  for (const file of files) {
    fileName = file.name;
    const splitName = fileName.split('.');
    const fileExtension = splitName[splitName.length - 1];
    if (fileExtension === 'csv') {
      filesToUpload.push(file);
    }
  }

  // 开始上传第一个文件
  uploadNextFile();
};

function uploadNextFile() {
  if (filesToUpload.length === 0){
  // 所有文件上传完成，清空上传区域
    progressArea.innerHTML = "";
    console.log("所有文件上传完成");
    return;
  }

  // 取出队列的第一个文件进行上传
  currentUpload = filesToUpload.shift(); // 获取当前要上传的文件并从队列中移除
  isLastFile = filesToUpload.length === 0; 
  const fileName = currentUpload.name;

  uploadFile(currentUpload, fileName, () => {
    // 上传完成后，上传下一个文件
    uploadNextFile();
  });
}

// file upload function
function uploadFile(file, name, nextFileCallback) {
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/upload/",true);
  let fileSize;

  xhr.upload.addEventListener("progress", ({ loaded, total }) => {
    const fileLoaded = Math.floor((loaded / total) * 100);
    const fileTotal = Math.floor(total / 1000);
    
    if (fileTotal < 1024) {
      fileSize = fileTotal + " KB";
    } else {
      fileSize = (loaded / (1024 * 1024)).toFixed(2) + " MB";
    }

    // 更新统一进度条
    const progressHTML = `
      <li class="row">
        <i class="fas fa-file-alt"></i>
        <div class="content">
          <div class="details">
            <span class="name">${name} • Uploading</span>
            <span class="percent">${fileLoaded}%</span>
          </div>
          <div class="progress-bar">
            <div class="progress" style="width: ${fileLoaded}%"></div>
          </div>
        </div>
      </li>
    `;
    uploadedArea.classList.add("onprogress");
    progressArea.innerHTML = progressHTML;
  });

  xhr.onload = () => {

    if (xhr.status === 200) {
        // 如果不是最后一个文件，添加上传完成项
        const uploadedHTML = `
          <li class="row">
            <div class="content upload">
              <i class="fas fa-file-alt"></i>
              <div class="details">
                <span class="name">${name} • Uploaded</span>
                <span class="size">${fileSize}</span>
              </div>
            </div>
            <i class="fas fa-check"></i>
          </li>
        `;
        uploadedArea.insertAdjacentHTML("afterbegin", uploadedHTML);
    } else {
      const uploadedHTML = `
          <li class="row">
            <div class="content upload">
              <i class="fas fa-file-alt"></i>
              <div class="details">
                <span class="name">${name} • Error </span>
                <span class="size">${fileSize}</span>
              </div>
            </div>
          </li>
        `;
        uploadedArea.insertAdjacentHTML("afterbegin", uploadedHTML);
    }
    // 执行回调函数，准备上传下一个文件
    nextFileCallback();
  };

  const formData = new FormData();
  formData.append("file", file);
  xhr.send(formData);
}