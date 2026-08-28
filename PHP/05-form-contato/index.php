<?php
// 05 - Form de contato: POST, validação, filter_var, htmlspecialchars, trim
$nome = trim($_POST['nome'] ?? '');
$email = trim($_POST['email'] ?? '');
$msg = trim($_POST['mensagem'] ?? '');
$erros = [];
$sucesso = false;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (mb_strlen($nome) < 3) $erros['nome'] = 'Nome precisa ter ao menos 3 caracteres.';
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $erros['email'] = 'E-mail inválido.';
    if (mb_strlen($msg) < 10) $erros['mensagem'] = 'Mensagem precisa ter ao menos 10 caracteres.';
    if (empty($erros)) $sucesso = true;
}
?>
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Form Contato PHP</title>
<style>body{font-family:system-ui;max-width:520px;margin:40px auto}label{display:block;margin:10px 0}input,textarea{width:100%;padding:8px} .erro{color:#c00;font-size:.9em} .ok{background:#dfd;padding:10px}</style>
</head>
<body>
<h1>05 - Formulário de Contato</h1>
<p>Conceitos: <code>$_POST</code>, <code>filter_var</code>, <code>trim</code>, <code>htmlspecialchars</code>, validação.</p>
<?php if ($sucesso): ?>
  <p class="ok">Obrigado, <?= htmlspecialchars($nome) ?>! Mensagem recebida.</p>
<?php else: ?>
<form method="post" novalidate>
  <label>Nome
    <input name="nome" value="<?= htmlspecialchars($nome) ?>">
    <?php if (isset($erros['nome'])): ?><span class="erro"><?= $erros['nome'] ?></span><?php endif; ?>
  </label>
  <label>E-mail
    <input name="email" value="<?= htmlspecialchars($email) ?>">
    <?php if (isset($erros['email'])): ?><span class="erro"><?= $erros['email'] ?></span><?php endif; ?>
  </label>
  <label>Mensagem
    <textarea name="mensagem" rows="4"><?= htmlspecialchars($msg) ?></textarea>
    <?php if (isset($erros['mensagem'])): ?><span class="erro"><?= $erros['mensagem'] ?></span><?php endif; ?>
  </label>
  <button type="submit">Enviar</button>
</form>
<?php endif; ?>
</body>
</html>
