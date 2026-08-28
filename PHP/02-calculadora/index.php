<?php
// 02 - Calculadora: $_GET, funções, validação

function calcular(float $a, float $b, string $op): ?float {
    return match ($op) {
        '+' => $a + $b,
        '-' => $a - $b,
        '*' => $a * $b,
        '/' => $b != 0 ? $a / $b : null,
        default => null,
    };
}

$a = isset($_GET['a']) ? trim($_GET['a']) : '';
$b = isset($_GET['b']) ? trim($_GET['b']) : '';
$op = $_GET['op'] ?? '+';
$erro = null;
$resultado = null;

if ($a !== '' || $b !== '') {
    if (!is_numeric($a) || !is_numeric($b)) {
        $erro = 'Digite dois números válidos.';
    } elseif (!in_array($op, ['+', '-', '*', '/'], true)) {
        $erro = 'Operação inválida.';
    } else {
        $resultado = calcular((float)$a, (float)$b, $op);
        if ($resultado === null) {
            $erro = 'Erro: divisão por zero ou operação inválida.';
        }
    }
}
?>
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Calculadora PHP</title>
<style>body{font-family:system-ui;max-width:480px;margin:40px auto}input,select,button{padding:8px;margin:4px} .erro{color:#c00} .ok{color:#080;font-weight:bold}</style>
</head>
<body>
<h1>02 - Calculadora</h1>
<p>Conceitos: <code>$_GET</code>, <code>is_numeric</code>, <code>match</code>, funções.</p>
<form method="get">
  <input name="a" value="<?= htmlspecialchars($a) ?>" placeholder="Número A" required>
  <select name="op">
    <?php foreach (['+', '-', '*', '/'] as $o): ?>
      <option value="<?= $o ?>" <?= $op === $o ? 'selected' : '' ?>><?= $o ?></option>
    <?php endforeach; ?>
  </select>
  <input name="b" value="<?= htmlspecialchars($b) ?>" placeholder="Número B" required>
  <button type="submit">Calcular</button>
</form>
<?php if ($erro): ?><p class="erro"><?= htmlspecialchars($erro) ?></p><?php endif; ?>
<?php if ($resultado !== null && !$erro): ?><p class="ok">Resultado: <?= htmlspecialchars((string)$resultado) ?></p><?php endif; ?>
<p><small>Dica: rode com <code>php -S localhost:8000</code> dentro da pasta.</small></p>
</body>
</html>
