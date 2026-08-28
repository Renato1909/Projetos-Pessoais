<?php
// 04 - Lista de compras: arrays, $_POST, foreach, htmlspecialchars, sessão simples via array
session_start();
if (!isset($_SESSION['lista'])) $_SESSION['lista'] = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $item = trim($_POST['item'] ?? '');
    $acao = $_POST['acao'] ?? 'add';
    if ($acao === 'add' && $item !== '') {
        $_SESSION['lista'][] = $item;
    } elseif ($acao === 'limpar') {
        $_SESSION['lista'] = [];
    } elseif ($acao === 'remover' && isset($_POST['idx'])) {
        $idx = (int)$_POST['idx'];
        if (isset($_SESSION['lista'][$idx])) {
            array_splice($_SESSION['lista'], $idx, 1);
        }
    }
    header('Location: ' . $_SERVER['PHP_SELF']);
    exit;
}
$lista = $_SESSION['lista'];
?>
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Lista de Compras PHP</title>
<style>body{font-family:system-ui;max-width:520px;margin:40px auto}ul{padding-left:20px}li{margin:4px 0}button{padding:6px 10px}</style>
</head>
<body>
<h1>04 - Lista de Compras</h1>
<p>Conceitos: <code>array</code>, <code>$_POST</code>, <code>foreach</code>, <code>htmlspecialchars</code>, <code>$_SESSION</code>.</p>
<form method="post">
  <input name="item" placeholder="Ex: Arroz" required>
  <button type="submit" name="acao" value="add">Adicionar</button>
  <button type="submit" name="acao" value="limpar">Limpar tudo</button>
</form>
<ul>
  <?php foreach ($lista as $i => $item): ?>
    <li>
      <?= htmlspecialchars($item) ?>
      <form method="post" style="display:inline">
        <input type="hidden" name="idx" value="<?= $i ?>">
        <button type="submit" name="acao" value="remover">x</button>
      </form>
    </li>
  <?php endforeach; ?>
  <?php if (empty($lista)): ?><li><em>Nenhum item ainda.</em></li><?php endif; ?>
</ul>
</body>
</html>
