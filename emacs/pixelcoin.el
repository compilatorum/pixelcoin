;;; pixelcoin.el --- Interface Generativa do PixelCoin para Emacs / Org-mode -*- lexical-binding: t; -*-

;; Author: Compilatorum Ecosystem
;; Version: 0.3.0
;; Package-Requires: ((emacs "27.1") (org "9.4"))
;; Keywords: outlines, hypermedia, economic-intelligence, compilatorum

;;; Commentary:
;; Integra o PixelCoin (Camada 6 — Renderizador Emacs / Org-mode) diretamente
;; ao fluxo de trabalho do desenvolvedor no Emacs.
;;
;; Comandos interativos:
;; - `M-x pixelcoin-prompt`: Formula uma pergunta ao PixelCoin e abre o buffer
;;   Org-mode estruturado com os 3 níveis da Compressão Semântica, tabelas de
;;   experimentos (`TESTAR`, `VALIDAR`, `PREPARAR`), links para fontes e hashes SHA-256.
;; - `M-x pixelcoin-portfolio-summary`: Abre o panorama completo do Compilatorum.

;;; Code:

(require 'org)

(defgroup pixelcoin nil
  "PixelCoin — Interface Generativa de Inteligência Econômica no Emacs."
  :group 'org
  :prefix "pixelcoin-")

(defcustom pixelcoin-project-root "/home/sukata/pixelcoin"
  "Caminho absoluto do repositório PixelCoin."
  :type 'directory
  :group 'pixelcoin)

(defcustom pixelcoin-default-perspective "executiva"
  "Perspectiva padrão para síntese (`executiva`, `desenvolvedor` ou `cientifica`)."
  :type '(choice (const "executiva")
                 (const "desenvolvedor")
                 (const "cientifica"))
  :group 'pixelcoin)

;;;###autoload
(defun pixelcoin-prompt (query &optional perspective)
  "Executa um QUERY generativo no PixelCoin e exibe o relatório em `org-mode`."
  (interactive
   (list (read-string "PixelCoin Prompt: "
                      "Tenho pouco orçamento para desenvolver o Compilatorum. Compare minhas opções e encontre a ação que mais reduz incerteza por unidade de recurso.")
         (completing-read "Perspectiva: " '("executiva" "desenvolvedor" "cientifica")
                          nil t nil nil pixelcoin-default-perspective)))
  (let* ((persp (or perspective pixelcoin-default-perspective))
         (default-directory pixelcoin-project-root)
         (process-environment (cons (concat "PYTHONPATH=" pixelcoin-project-root "/src")
                                    process-environment))
         (buf (get-buffer-create "*PixelCoin Org Interface*")))
    (with-current-buffer buf
      (let ((inhibit-read-only t))
        (erase-buffer)
        (let ((exit-code (call-process "python3" nil t nil
                                       "-m" "pixelcoin" "render"
                                       "--surface" "org"
                                       "--perspective" persp
                                       "--prompt" query)))
          (if (zerop exit-code)
              (progn
                (org-mode)
                (goto-char (point-min)))
            (error "Falha ao executar PixelCoin CLI (código %d)" exit-code)))))
    (pop-to-buffer buf)))

;;;###autoload
(defun pixelcoin-portfolio-summary ()
  "Abre o resumo do portfólio do Compilatorum em uma tela no Emacs Org-mode."
  (interactive)
  (pixelcoin-prompt "Resuma meu portfólio em uma tela." "executiva"))

(provide 'pixelcoin)
;;; pixelcoin.el ends here
