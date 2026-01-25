// AIDocGenius 前端 JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const operationType = document.getElementById('operationType');
    const targetLanguageContainer = document.getElementById('targetLanguageContainer');
    const outputFormatContainer = document.getElementById('outputFormatContainer');
    const processButton = document.getElementById('processButton');
    const resultCard = document.getElementById('resultCard');
    const resultContent = document.getElementById('resultContent');

    // 文件上传
    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.backgroundColor = '#e9ecef';
    });
    dropZone.addEventListener('dragleave', () => {
        dropZone.style.backgroundColor = '#f8f9fa';
    });
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.backgroundColor = '#f8f9fa';
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
        }
    });

    // 操作类型变化
    operationType.addEventListener('change', function() {
        const op = this.value;
        targetLanguageContainer.style.display = op === 'translate' ? 'block' : 'none';
        outputFormatContainer.style.display = op === 'convert' ? 'block' : 'none';
    });

    // 处理文档
    processButton.addEventListener('click', async function() {
        const file = fileInput.files[0];
        if (!file) {
            alert('请先选择文件');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        const op = operationType.value;
        let url = '';
        let params = {};

        switch (op) {
            case 'summarize':
                url = '/summarize';
                break;
            case 'translate':
                url = '/translate';
                params.target_language = document.getElementById('targetLanguage').value;
                break;
            case 'analyze':
                url = '/analyze';
                break;
            case 'convert':
                url = '/convert';
                params.output_format = document.getElementById('outputFormat').value;
                break;
        }

        // 添加参数到 URL
        const queryString = new URLSearchParams(params).toString();
        if (queryString) {
            url += '?' + queryString;
        }

        processButton.disabled = true;
        processButton.textContent = '处理中...';

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            displayResult(data, op);
        } catch (error) {
            resultCard.style.display = 'block';
            resultContent.innerHTML = `<div class="alert alert-danger">错误: ${error.message}</div>`;
        } finally {
            processButton.disabled = false;
            processButton.textContent = '处理文档';
        }
    });

    function displayResult(data, operation) {
        resultCard.style.display = 'block';
        let html = '';

        switch (operation) {
            case 'summarize':
                html = `<div class="alert alert-success"><strong>摘要：</strong><p>${data.summary || data}</p></div>`;
                break;
            case 'translate':
                html = `<div class="alert alert-info"><strong>翻译结果：</strong><p>${data.translation || data}</p></div>`;
                break;
            case 'analyze':
                html = '<div class="alert alert-primary"><strong>分析结果：</strong><pre>' + 
                       JSON.stringify(data, null, 2) + '</pre></div>';
                break;
            case 'convert':
                html = `<div class="alert alert-success"><strong>转换完成</strong><p>${data.converted_content || '转换成功'}</p></div>`;
                break;
        }

        resultContent.innerHTML = html;
    }
});
