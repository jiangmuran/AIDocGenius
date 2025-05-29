document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const operationType = document.getElementById('operationType');
    const targetLanguageContainer = document.getElementById('targetLanguageContainer');
    const outputFormatContainer = document.getElementById('outputFormatContainer');
    const processButton = document.getElementById('processButton');
    const resultCard = document.getElementById('resultCard');
    const resultContent = document.getElementById('resultContent');

    // 处理拖放
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('bg-light');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('bg-light');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('bg-light');
        const file = e.dataTransfer.files[0];
        handleFile(file);
    });

    // 处理点击上传
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        handleFile(file);
    });

    // 操作类型变更处理
    operationType.addEventListener('change', () => {
        updateUI();
    });

    // 处理文件
    function handleFile(file) {
        if (!file) return;
        dropZone.innerHTML = `
            <i class="bi bi-file-earmark-check text-success display-4"></i>
            <p class="mb-0">${file.name}</p>
        `;
        updateUI();
    }

    // 更新UI显示
    function updateUI() {
        const operation = operationType.value;
        targetLanguageContainer.style.display = operation === 'translate' ? 'block' : 'none';
        outputFormatContainer.style.display = operation === 'convert' ? 'block' : 'none';
    }

    // 处理文档
    processButton.addEventListener('click', async () => {
        const file = fileInput.files[0] || null;
        if (!file) {
            alert('请先选择文件');
            return;
        }

        const operation = operationType.value;
        const formData = new FormData();
        formData.append('file', file);

        let endpoint = '';
        let additionalParams = {};

        switch (operation) {
            case 'summarize':
                endpoint = '/summarize';
                break;
            case 'translate':
                endpoint = '/translate';
                additionalParams = {
                    target_language: document.getElementById('targetLanguage').value
                };
                break;
            case 'analyze':
                endpoint = '/analyze';
                break;
            case 'convert':
                endpoint = '/convert';
                additionalParams = {
                    output_format: document.getElementById('outputFormat').value
                };
                break;
        }

        try {
            processButton.disabled = true;
            processButton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> 处理中...';

            const response = await fetch(endpoint + '?' + new URLSearchParams(additionalParams), {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.detail || '处理失败');
            }

            displayResult(result, operation);
        } catch (error) {
            alert('错误：' + error.message);
        } finally {
            processButton.disabled = false;
            processButton.textContent = '处理文档';
        }
    });

    // 显示结果
    function displayResult(result, operation) {
        resultCard.style.display = 'block';
        let content = '';

        switch (operation) {
            case 'summarize':
                content = `<h6>文档摘要：</h6><p>${result.summary}</p>`;
                break;
            case 'translate':
                content = `<h6>翻译结果：</h6><p>${result.translation}</p>`;
                break;
            case 'analyze':
                content = `
                    <h6>文档分析：</h6>
                    <ul>
                        <li>可读性评分：${result.readability.score}</li>
                        <li>建议：${result.readability.suggestion}</li>
                        <li>段落数：${result.structure.paragraph_count}</li>
                        <li>句子数：${result.structure.sentence_count}</li>
                        <li>结构评分：${result.structure.structure_score}</li>
                    </ul>
                    <h6>关键词：</h6>
                    <p>${result.keywords.slice(0, 5).map(k => k.word).join(', ')}</p>
                `;
                break;
            case 'convert':
                content = `<h6>转换完成</h6><p>文件已成功转换，请检查下载内容。</p>`;
                break;
        }

        resultContent.innerHTML = content;
        resultContent.scrollIntoView({ behavior: 'smooth' });
    }
}); 