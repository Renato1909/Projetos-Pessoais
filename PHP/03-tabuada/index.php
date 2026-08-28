<?php
// 03 - Tabuada: for, foreach, include, $_GET
$num = isset($_GET['n']) ? (int)$_GET['n'] : 5;
$num = max(1, min(100, $num)); // limita 1..100
?>
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Tabuada PHP</title>
<style>body{font-family:system-ui;max-width:480px;margin:40px auto}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:6px;text-align:center}</style>
</head>
<body>
<h1>03 - Tabuada</h1>
<p>Conceitos: <code>for</code>, <code>foreach</code>, <code>include</code>, sanitização com <code>(int)</code>.</p>
<form method="get">
  <label>Número: <input type="number" name="n" value="<?= $num ?>" min="1" max="100" required></label>
  <button type="submit">Gerar</button>
</form>
<table>
  <tr><th>Conta</th><th>Resultado</th></tr>
  <?php for ($i = 1; $i <= 10; $i++): ?>
    <tr><td><?= $num ?> x <?= $i ?></td><td><?= $num * $i ?></td></tr>
  <?php endfor; ?>
</table>
<p><small>Desafio: crie <code>header.php</code> e <code>footer.php</code> e use <code>include</code>.</small></p>
</body>
</html>
