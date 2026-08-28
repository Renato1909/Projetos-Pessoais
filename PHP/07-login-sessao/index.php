<?php
// 07 - Login com sessão: session_start, password_hash/verify, header Location
session_start();

// usuário demo (em projeto real viria de BD)
define('DEMO_USER', 'admin');
define('DEMO_PASS_HASH', password_hash('admin123', PASSWORD_DEFAULT));

$erro = null;
$acao = $_GET['acao'] ?? $_POST['acao'] ?? '';

if ($acao === 'logout') {
    session_destroy();
    header('Location: ' . strtok($_SERVER['REQUEST_URI'], '?'));
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && ($acao === 'login' || $acao === '')) {
    $user = trim($_POST['user'] ?? '');
    $pass = $_POST['pass'] ?? '';
    if ($user === DEMO_USER && password_verify($pass, DEMO_PASS_HASH)) {
        $_SESSION['logado'] = $user;
        header('Location: ' . $_SERVER['PHP_SELF']);
        exit;
    } else {
        $erro = 'Usuário ou senha inválidos. Dica: admin / admin123';
    }
}

$logado = isset($_SESSION['logado']);
?>
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Login PHP</title>
<style>body{font-family:system-ui;max-width:480px;margin:40px auto}input,button{padding:8px;margin:4px 0;width:100%} .erro{color:#c00} .ok{background:#dfd;padding:10px}</style>
</head>
<body>
<h1>07 - Login com Sessão</h1>
<p>Conceitos: <code>session_start</code>, <code>password_hash/verify</code>, <code>header(Location)</code>, área protegida.</p>
<?php if ($logado): ?>
  <p class="ok">Olá, <?= htmlspecialchars($_SESSION['logado']) ?>! Você está logado.</p>
  <p>Conteúdo protegido: 🎉</p>
  <a href="?acao=logout"><button>Sair</button></a>
<?php else: ?>
  <?php if ($erro): ?><p class="erro"><?= htmlspecialchars($erro) ?></p><?php endif; ?>
  <form method="post">
    <input name="user" placeholder="Usuário" value="admin" required>
    <input name="pass" type="password" placeholder="Senha" required>
    <button type="submit" name="acao" value="login">Entrar</button>
  </form>
  <p><small>Credenciais demo: <code>admin</code> / <code>admin123</code></small></p>
<?php endif; ?>
</body>
</html>
