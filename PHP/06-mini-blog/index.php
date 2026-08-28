<?php
// 06 - Mini blog: JSON como "banco", file_get_contents, json_encode/decode, CRUD básico
define('DATA_FILE', __DIR__ . '/posts.json');

function carregarPosts(): array {
    if (!file_exists(DATA_FILE)) return [];
    $json = file_get_contents(DATA_FILE);
    $data = json_decode($json, true);
    return is_array($data) ? $data : [];
}
function salvarPosts(array $posts): void {
    file_put_contents(DATA_FILE, json_encode($posts, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);
}

$erro = null;
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $acao = $_POST['acao'] ?? 'criar';
    $posts = carregarPosts();
    if ($acao === 'criar') {
        $titulo = trim($_POST['titulo'] ?? '');
        $texto = trim($_POST['texto'] ?? '');
        if (mb_strlen($titulo) < 3) $erro = 'Título muito curto.';
        elseif (mb_strlen($texto) < 10) $erro = 'Texto muito curto.';
        else {
            $posts[] = ['id' => time() . rand(100, 999), 'titulo' => $titulo, 'texto' => $texto, 'data' => date('Y-m-d H:i')];
            salvarPosts($posts);
            header('Location: ' . $_SERVER['PHP_SELF']);
            exit;
        }
    } elseif ($acao === 'apagar' && isset($_POST['id'])) {
        $posts = array_values(array_filter($posts, fn($p) => (string)$p['id'] !== (string)$_POST['id']));
        salvarPosts($posts);
        header('Location: ' . $_SERVER['PHP_SELF']);
        exit;
    }
}
$posts = carregarPosts();
$posts = array_reverse($posts); // mais novos primeiro
?>
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Mini Blog PHP</title>
<style>body{font-family:system-ui;max-width:640px;margin:40px auto}article{border:1px solid #ddd;padding:12px;margin:12px 0}input,textarea{width:100%;padding:8px;margin:4px 0}button{padding:6px 12px}</style>
</head>
<body>
<h1>06 - Mini Blog (JSON)</h1>
<p>Conceitos: <code>file_get_contents</code>, <code>json_encode/decode</code>, <code>file_put_contents LOCK_EX</code>, CRUD.</p>
<?php if ($erro): ?><p style="color:#c00"><?= htmlspecialchars($erro) ?></p><?php endif; ?>
<form method="post">
  <input name="titulo" placeholder="Título" required>
  <textarea name="texto" rows="3" placeholder="Texto do post" required></textarea>
  <button type="submit" name="acao" value="criar">Publicar</button>
</form>
<hr>
<?php if (empty($posts)): ?><p><em>Nenhum post ainda.</em></p><?php endif; ?>
<?php foreach ($posts as $p): ?>
<article>
  <h3><?= htmlspecialchars($p['titulo']) ?> <small style="color:#666"><?= htmlspecialchars($p['data']) ?></small></h3>
  <p><?= nl2br(htmlspecialchars($p['texto'])) ?></p>
  <form method="post" onsubmit="return confirm('Apagar?')">
    <input type="hidden" name="id" value="<?= htmlspecialchars($p['id']) ?>">
    <button type="submit" name="acao" value="apagar">Apagar</button>
  </form>
</article>
<?php endforeach; ?>
<p><small>Dados em <code>posts.json</code> (ignorado no git se quiser). Próximo nível: trocar JSON por SQLite + PDO.</small></p>
</body>
</html>
