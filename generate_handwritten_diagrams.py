import os
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend, crucial for headless execution
import matplotlib.pyplot as plt

def generate_architecture_diagram():
    with plt.xkcd():
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        # Draw Browser / Client Box
        ax.text(2, 8.5, "Browser / Client\n(HTML, CSS, JS)", ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.5", fc="#ffe6e6", ec="#cc0000", lw=2))

        # Draw FastAPI / Jinja2 Box
        ax.text(5, 5, "FastAPI Web Backend\n(router.py, models.py,\nJinja2 templates)", ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.5", fc="#e6f2ff", ec="#0066cc", lw=2))

        # Draw Database Box
        ax.text(8, 1.5, "SQLite Database\n(app.db)", ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.5", fc="#e6ffe6", ec="#009933", lw=2))

        # Draw connecting arrows
        ax.annotate("", xy=(4, 6), xytext=(2, 8),
                    arrowprops=dict(arrowstyle="->", lw=2, color="#555555", connectionstyle="arc3,rad=-0.1"))
        ax.annotate("", xy=(2.3, 8.2), xytext=(4.3, 6.2),
                    arrowprops=dict(arrowstyle="->", lw=2, color="#555555", connectionstyle="arc3,rad=-0.1"))

        ax.annotate("", xy=(7.2, 2.3), xytext=(5.8, 4.2),
                    arrowprops=dict(arrowstyle="->", lw=2, color="#555555", connectionstyle="arc3,rad=-0.1"))
        ax.annotate("", xy=(6, 4.5), xytext=(7.4, 2.6),
                    arrowprops=dict(arrowstyle="->", lw=2, color="#555555", connectionstyle="arc3,rad=-0.1"))

        # Add notes
        ax.text(2, 6.5, "HTTP GET / POST\n(Jinja2 HTML)", fontsize=9, ha='center')
        ax.text(8, 4, "SQL Queries\n(sqlite3)", fontsize=9, ha='center')

        plt.title("Piattaforma di Sharing - Architettura a 3 Livelli", fontsize=14, pad=20)
        os.makedirs("docs/images", exist_ok=True)
        plt.tight_layout()
        plt.savefig("docs/images/architecture.png", dpi=150)
        plt.close()
        print("Architettura diagram generated.")

def generate_lifecycle_diagram():
    with plt.xkcd():
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 6)
        ax.axis('off')

        # Draw States
        # 1. In Attesa
        ax.text(2, 4, "IN ATTESA\n(Stato iniziale)", ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.4", fc="#fff2cc", ec="#d6b656", lw=2))

        # 2. Rifiutata
        ax.text(2, 1.5, "RIFIUTATA\n(Free object)", ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.4", fc="#f8cecc", ec="#b85450", lw=2))

        # 3. Approvata / Attiva
        ax.text(6, 4, "APPROVATA / ATTIVA\n(In Uso)", ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.4", fc="#d5e8d4", ec="#82b366", lw=2))

        # 4. Conclusa
        ax.text(10, 4, "CONCLUSA\n(Free object)", ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.4", fc="#e1d5e7", ec="#9673a6", lw=2))

        # 5. Penale
        ax.text(8, 1.5, "APPLICA PENALE\n(Ritardo/Danni)", ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.4", fc="#f8cecc", ec="#b85450", lw=2))

        # Draw Arrows
        # In attesa -> Approvata
        ax.annotate("Proprietario\napprova", xy=(4.5, 4), xytext=(3.3, 4),
                    arrowprops=dict(arrowstyle="->", lw=2, color="#555555"))

        # In attesa -> Rifiutata
        ax.annotate("Proprietario\nrifiuta", xy=(2, 2.1), xytext=(2, 3.4),
                    arrowprops=dict(arrowstyle="->", lw=2, color="#555555"))

        # Approvata -> Conclusa
        ax.annotate("Restituzione\nin tempo", xy=(8.5, 4), xytext=(7.5, 4),
                    arrowprops=dict(arrowstyle="->", lw=2, color="#555555"))

        # Approvata -> Penale
        ax.annotate("Scadenza superata", xy=(7.7, 2.1), xytext=(6.5, 3.4),
                    arrowprops=dict(arrowstyle="->", lw=2, color="#555555"))

        # Penale -> Conclusa
        ax.annotate("Penale pagata", xy=(9.5, 3.4), xytext=(8.5, 2.1),
                    arrowprops=dict(arrowstyle="->", lw=2, color="#555555"))

        plt.title("Ciclo di Vita della Prenotazione e Gestione Penali", fontsize=14, pad=20)
        plt.tight_layout()
        plt.savefig("docs/images/lifecycle.png", dpi=150)
        plt.close()
        print("Lifecycle diagram generated.")

if __name__ == "__main__":
    generate_architecture_diagram()
    generate_lifecycle_diagram()
