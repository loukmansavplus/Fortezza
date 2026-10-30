<?php
// Réception des formulaires Devis / Contact.
// Envoie un email à Fortezza + un accusé de réception au visiteur.
declare(strict_types=1);

const TO_DEVIS   = 'devis@fortezza.bj';
const TO_CONTACT = 'contact@fortezza.bj';
const FROM       = 'no-reply@fortezza.bj'; // doit exister sur le domaine pour une bonne délivrabilité
const MAX_FILE   = 5 * 1024 * 1024;

$wantsJson = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');

function done(bool $ok, string $err = ''): void {
    global $wantsJson;
    if ($wantsJson) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'error' => $err]);
    } else {
        header('Location: ' . ($ok ? '/merci' : '/contact'));
    }
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); exit; }
if (!empty($_POST['website'])) { done(true); }          // honeypot : on fait semblant que tout va bien

function clean(string $k): string {
    return trim(preg_replace('/[\r\n]+/', ' ', strip_tags((string)($_POST[$k] ?? ''))));
}

$form  = clean('form') === 'contact' ? 'contact' : 'devis';
$nom   = clean('nom');
$email = filter_var(clean('email'), FILTER_VALIDATE_EMAIL);
$tel   = clean('tel');
$besoin = trim(strip_tags((string)($_POST['besoin'] ?? '')));

if ($nom === '' || !$email || $besoin === '' || empty($_POST['consent'])) { done(false, 'invalid'); }

// anti-flood simple : 1 envoi / 20 s par session
session_start();
if (isset($_SESSION['last']) && time() - $_SESSION['last'] < 20) { done(false, 'rate'); }
$_SESSION['last'] = time();

$lines = ["Nom : $nom", "Email : $email", "Téléphone : $tel"];
foreach (['entreprise' => 'Entreprise', 'type' => 'Type de client', 'service' => 'Service', 'budget' => 'Budget (FCFA)', 'delai' => 'Délai'] as $k => $l) {
    if (clean($k) !== '') $lines[] = "$l : " . clean($k);
}
$lines[] = "\nMessage :\n$besoin";
$text = implode("\n", $lines);
$subject = ($form === 'devis' ? 'Demande de devis' : 'Message de contact') . " - $nom";
$to = $form === 'devis' ? TO_DEVIS : TO_CONTACT;

$headers = ['From: Site Fortezza <' . FROM . '>', 'Reply-To: ' . $email, 'MIME-Version: 1.0'];
$body = $text;

// pièce jointe optionnelle (PDF / image, 5 Mo max)
if (!empty($_FILES['fichier']['tmp_name']) && $_FILES['fichier']['error'] === UPLOAD_ERR_OK) {
    $f = $_FILES['fichier'];
    $mime = (new finfo(FILEINFO_MIME_TYPE))->file($f['tmp_name']);
    if ($f['size'] > MAX_FILE || !preg_match('#^(application/pdf|image/(jpeg|png|webp))$#', $mime)) { done(false, 'file'); }
    $b = 'fz' . bin2hex(random_bytes(8));
    $headers[] = "Content-Type: multipart/mixed; boundary=\"$b\"";
    $name = preg_replace('/[^A-Za-z0-9._-]/', '_', $f['name']);
    $body = "--$b\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n$text\r\n"
          . "--$b\r\nContent-Type: $mime; name=\"$name\"\r\nContent-Transfer-Encoding: base64\r\n"
          . "Content-Disposition: attachment; filename=\"$name\"\r\n\r\n"
          . chunk_split(base64_encode(file_get_contents($f['tmp_name']))) . "--$b--";
} else {
    $headers[] = 'Content-Type: text/plain; charset=UTF-8';
}

$sent = mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $headers));
if (!$sent) { done(false, 'mail'); }

// accusé de réception
$ack = "Bonjour $nom,\n\nNous avons bien reçu votre demande et nous revenons vers vous très rapidement.\n\n"
     . "Pour une réponse immédiate, écrivez-nous sur WhatsApp.\n\nL'équipe Fortezza\nL'Excellence Technologique\nhttps://fortezza.bj";
mail((string)$email, '=?UTF-8?B?' . base64_encode('Fortezza - Nous avons bien reçu votre demande') . '?=', $ack,
     "From: Fortezza <" . FROM . ">\r\nContent-Type: text/plain; charset=UTF-8");

done(true);
