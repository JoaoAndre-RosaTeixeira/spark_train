function handleDrop(event) {
  event.preventDefault();
  const files = event.dataTransfer.files;
  handleFiles(files);
}

function handleDragOver(event) {
  event.preventDefault();
}

function handleFileSelect() {
  const files = document.getElementById('file-input').files;
  handleFiles(files);
}

function handleFiles(files) {
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    uploadFile(file);
  }
}

function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);

  fetch('/upload', {
    method: 'POST',
    body: formData
  })
  .then(response => {
    if (response.ok) {
      console.log('Fichier envoyé avec succès');
      // Ajoutez ici le code supplémentaire que vous souhaitez exécuter après avoir envoyé le fichier
    } else {
      console.error('Erreur lors de l\'envoi du fichier');
    }
  })
  .catch(error => {
    console.error('Erreur lors de l\'envoi du fichier:', error);
  });
}
