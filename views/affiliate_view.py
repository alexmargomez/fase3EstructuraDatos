"""AffiliateView main window ('Caja Compensándote – Control de Afiliados')."""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional

from controllers.affiliate_controller import (
    COURSE_CODE,
    COURSE_NAME,
    DATA_STRUCTURES,
    DESIRED_SERVICES,
    EMPLOYMENT_MODES,
    ID_TYPES,
    STUDENT_NAME,
    AffiliateController,
)
from views.theme import (
    ACCENT_AMBER,
    ACCENT_CYAN,
    ACCENT_GREEN,
    ACCENT_RED,
    ACCENT_SLATE,
    BG_CARD,
    BG_INPUT,
    BG_PRIMARY,
    BG_SECONDARY,
    DateEntrySpinbox,
    FG_PRIMARY,
    FG_SECONDARY,
    FONT_FAMILY,
    MAIN_WINDOW_TITLE,
    apply_theme,
)


class AffiliateView:
    """Main data entry GUI managing the Treeview and delegating actions to AffiliateController."""

    def __init__(self, root: tk.Tk, controller: AffiliateController) -> None:
        self.root = root
        self.controller = controller

        self.id_type_var = tk.StringVar(value=ID_TYPES[0])
        self.id_number_var = tk.StringVar()
        self.full_name_var = tk.StringVar()
        self.current_income_var = tk.StringVar()
        self.employment_mode_var = tk.StringVar(value=EMPLOYMENT_MODES[0])
        self.desired_service_var = tk.StringVar(value=DESIRED_SERVICES[0])
        self.affiliation_fee_var = tk.StringVar(value="$0.00")
        self.structure_var = tk.StringVar(value=DATA_STRUCTURES[0])
        self.report_var = tk.StringVar(value="")
        self.status_var = tk.StringVar(
            value="Listo — Diligencie el formulario y presione 'Registrar'."
        )

        self._configure_window()
        self._build_ui()
        self._bind_events()
        self.refresh_treeview()
        self.id_number_entry.focus_set()

    def _configure_window(self) -> None:
        """Configures title, geometry, and minimum dimensions of the main window."""
        apply_theme(self.root)
        self.root.title(MAIN_WINDOW_TITLE)
        self.root.configure(bg=BG_PRIMARY)
        self.root.resizable(True, True)

        width, height = 1200, 730
        pos_x = max(0, (self.root.winfo_screenwidth() - width) // 2)
        pos_y = max(0, (self.root.winfo_screenheight() - height) // 2)
        self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        self.root.minsize(1040, 660)

    def _build_ui(self) -> None:
        """Builds the header, left capture form, right Treeview panel, and status bar."""
        header = tk.Frame(self.root, bg=BG_SECONDARY, padx=20, pady=10)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Caja Compensándote — Control de Afiliados",
            bg=BG_SECONDARY,
            fg=ACCENT_CYAN,
            font=(FONT_FAMILY, 14, "bold"),
        ).pack(side=tk.LEFT)

        tk.Label(
            header,
            text=f"{STUDENT_NAME}  |  {COURSE_NAME} {COURSE_CODE}",
            bg=BG_SECONDARY,
            fg=FG_SECONDARY,
            font=(FONT_FAMILY, 9),
        ).pack(side=tk.RIGHT)

        tk.Frame(self.root, bg=ACCENT_CYAN, height=2).pack(fill=tk.X)

        content = tk.Frame(self.root, bg=BG_PRIMARY, padx=14, pady=10)
        content.pack(fill=tk.BOTH, expand=True)
        content.columnconfigure(0, weight=0, minsize=360)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        self._build_left_panel(content)
        self._build_right_panel(content)

        status_bar = tk.Frame(self.root, bg=BG_SECONDARY, padx=14, pady=4)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(
            status_bar,
            textvariable=self.status_var,
            bg=BG_SECONDARY,
            fg=FG_SECONDARY,
            font=(FONT_FAMILY, 8),
            anchor="w",
        ).pack(fill=tk.X)

    def _build_left_panel(self, parent: tk.Frame) -> None:
        """Builds the data entry form controls on the left panel."""
        panel = tk.Frame(
            parent,
            bg=BG_SECONDARY,
            padx=14,
            pady=10,
            highlightbackground=BG_CARD,
            highlightthickness=1,
        )
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        vcmd_digits = (self.root.register(self.controller.is_valid_key_digits), "%P")
        vcmd_letters = (self.root.register(self.controller.is_valid_key_letters), "%P")
        vcmd_income = (self.root.register(self.controller.is_valid_key_income), "%P")

        ttk.Label(panel, text="1. Identificación del Afiliado", style="Section.TLabel").pack(
            fill=tk.X, pady=(0, 4)
        )

        id_row = tk.Frame(panel, bg=BG_SECONDARY)
        id_row.pack(fill=tk.X, pady=(0, 6))
        id_row.columnconfigure(0, weight=0, minsize=95)
        id_row.columnconfigure(1, weight=1)

        ttk.Label(id_row, text="Tipo ID:", style="Field.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 2)
        )
        ttk.Label(
            id_row,
            text="Número de Identificación (solo números):",
            style="Field.TLabel",
        ).grid(row=0, column=1, sticky="w", pady=(0, 2))

        self.id_type_combo = ttk.Combobox(
            id_row,
            textvariable=self.id_type_var,
            values=ID_TYPES,
            state="readonly",
            width=8,
        )
        self.id_type_combo.grid(row=1, column=0, sticky="ew", padx=(0, 8), ipady=2)

        self.id_number_entry = tk.Entry(
            id_row,
            textvariable=self.id_number_var,
            validate="key",
            validatecommand=vcmd_digits,
            bg=BG_INPUT,
            fg=FG_PRIMARY,
            insertbackground=FG_PRIMARY,
            relief="solid",
            bd=1,
            font=(FONT_FAMILY, 10),
        )
        self.id_number_entry.grid(row=1, column=1, sticky="ew", ipady=3)

        ttk.Label(
            panel,
            text="Nombre Completo (solo letras):",
            style="Field.TLabel",
        ).pack(fill=tk.X, pady=(2, 2))
        self.full_name_entry = tk.Entry(
            panel,
            textvariable=self.full_name_var,
            validate="key",
            validatecommand=vcmd_letters,
            bg=BG_INPUT,
            fg=FG_PRIMARY,
            insertbackground=FG_PRIMARY,
            relief="solid",
            bd=1,
            font=(FONT_FAMILY, 10),
        )
        self.full_name_entry.pack(fill=tk.X, ipady=3, pady=(0, 8))

        ttk.Label(panel, text="2. Datos Económicos y Servicio", style="Section.TLabel").pack(
            fill=tk.X, pady=(2, 4)
        )

        ttk.Label(
            panel,
            text="Ingresos Actuales ($) (solo números, mín. 1000000):",
            style="Field.TLabel",
        ).pack(fill=tk.X, pady=(2, 2))
        self.current_income_entry = tk.Entry(
            panel,
            textvariable=self.current_income_var,
            validate="key",
            validatecommand=vcmd_income,
            bg=BG_INPUT,
            fg=FG_PRIMARY,
            insertbackground=FG_PRIMARY,
            relief="solid",
            bd=1,
            font=(FONT_FAMILY, 10),
        )
        self.current_income_entry.pack(fill=tk.X, ipady=3, pady=(0, 6))

        ttk.Label(panel, text="Modalidad de Empleo:", style="Field.TLabel").pack(
            fill=tk.X, pady=(2, 2)
        )
        radio_frame = tk.Frame(panel, bg=BG_SECONDARY)
        radio_frame.pack(fill=tk.X, pady=(0, 6))
        ttk.Radiobutton(
            radio_frame,
            text="Empleado",
            variable=self.employment_mode_var,
            value="Empleado",
        ).pack(side=tk.LEFT, padx=(0, 16))
        ttk.Radiobutton(
            radio_frame,
            text="Independiente",
            variable=self.employment_mode_var,
            value="Independiente",
        ).pack(side=tk.LEFT)

        ttk.Label(panel, text="Servicio Deseado:", style="Field.TLabel").pack(
            fill=tk.X, pady=(2, 2)
        )
        self.desired_service_combo = ttk.Combobox(
            panel,
            textvariable=self.desired_service_var,
            values=DESIRED_SERVICES,
            state="readonly",
        )
        self.desired_service_combo.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(
            panel,
            text="Tarifa de Afiliación ($) — no editable:",
            style="Field.TLabel",
        ).pack(fill=tk.X, pady=(2, 2))
        self.affiliation_fee_entry = tk.Entry(
            panel,
            textvariable=self.affiliation_fee_var,
            state="readonly",
            readonlybackground=BG_CARD,
            fg=ACCENT_CYAN,
            font=(FONT_FAMILY, 10, "bold"),
            relief="solid",
            bd=1,
        )
        self.affiliation_fee_entry.pack(fill=tk.X, ipady=3, pady=(0, 8))

        ttk.Label(
            panel,
            text="3. Fecha de Afiliación (DateEntry + Spinbox)",
            style="Section.TLabel",
        ).pack(fill=tk.X, pady=(2, 4))
        self.date_selector = DateEntrySpinbox(panel)
        self.date_selector.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(
            panel,
            text="4. Estructura de Datos y Reporte",
            style="Section.TLabel",
        ).pack(fill=tk.X, pady=(2, 4))

        ttk.Label(panel, text="Ver Estructura:", style="Field.TLabel").pack(
            fill=tk.X, pady=(2, 2)
        )
        self.structure_combo = ttk.Combobox(
            panel,
            textvariable=self.structure_var,
            values=DATA_STRUCTURES,
            state="readonly",
        )
        self.structure_combo.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(panel, text="Reporte — no editable:", style="Field.TLabel").pack(
            fill=tk.X, pady=(2, 2)
        )
        self.report_entry = tk.Entry(
            panel,
            textvariable=self.report_var,
            state="readonly",
            readonlybackground=BG_CARD,
            fg="#FFD166",
            font=(FONT_FAMILY, 9, "bold"),
            relief="solid",
            bd=1,
        )
        self.report_entry.pack(fill=tk.X, ipady=3)

    def _build_right_panel(self, parent: tk.Frame) -> None:
        """Builds the right panel with the Treeview and the 5 action buttons."""
        right_panel = tk.Frame(parent, bg=BG_PRIMARY)
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.rowconfigure(1, weight=1)
        right_panel.columnconfigure(0, weight=1)

        table_header = tk.Frame(right_panel, bg=BG_SECONDARY, padx=14, pady=8)
        table_header.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        self.structure_banner_label = tk.Label(
            table_header,
            text="Estructura Activa: Pila (LIFO — Apilar / Desapilar)",
            bg=BG_SECONDARY,
            fg=ACCENT_CYAN,
            font=(FONT_FAMILY, 10, "bold"),
            anchor="w",
        )
        self.structure_banner_label.pack(side=tk.LEFT)

        tree_frame = tk.Frame(
            right_panel,
            bg=BG_SECONDARY,
            highlightbackground=BG_CARD,
            highlightthickness=1,
        )
        tree_frame.grid(row=1, column=0, sticky="nsew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        columns = (
            "id_type",
            "id_number",
            "full_name",
            "current_income",
            "desired_service",
            "employment_mode",
            "affiliation_fee",
            "affiliation_date",
        )
        self.treeview = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = (
            ("id_type", "Tipo ID", 65, "center"),
            ("id_number", "Número ID", 105, "center"),
            ("full_name", "Nombre Completo", 175, "w"),
            ("current_income", "Ingresos ($)", 115, "e"),
            ("desired_service", "Servicio Deseado", 150, "w"),
            ("employment_mode", "Modalidad", 100, "center"),
            ("affiliation_fee", "Tarifa ($)", 105, "e"),
            ("affiliation_date", "Fecha Afiliación", 105, "center"),
        )
        for col_id, title, width, anchor in headings:
            self.treeview.heading(col_id, text=title)
            self.treeview.column(col_id, width=width, minwidth=width, anchor=anchor)

        v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.treeview.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.treeview.xview)
        self.treeview.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.treeview.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        actions_frame = tk.Frame(right_panel, bg=BG_PRIMARY, pady=10)
        actions_frame.grid(row=2, column=0, sticky="ew")
        actions_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

        buttons = (
            ("Registrar", self.handle_register, ACCENT_CYAN, 0),
            ("Eliminar", self.handle_delete, ACCENT_RED, 1),
            ("Reporte", self.handle_report, ACCENT_GREEN, 2),
            ("Limpiar", self.handle_clear, ACCENT_AMBER, 3),
            ("Salir", self.handle_exit, ACCENT_SLATE, 4),
        )
        for text, cmd, color, col_idx in buttons:
            btn = tk.Button(
                actions_frame,
                text=text,
                command=cmd,
                bg=color,
                fg="#FFFFFF",
                activebackground=BG_CARD,
                activeforeground="#FFFFFF",
                font=(FONT_FAMILY, 10, "bold"),
                relief="flat",
                pady=10,
                cursor="hand2",
            )
            padx = (0, 6) if col_idx == 0 else ((6, 0) if col_idx == 4 else (6, 6))
            btn.grid(row=0, column=col_idx, sticky="ew", padx=padx)

    def _bind_events(self) -> None:
        """Binds reactive fee calculation and structure change events."""
        self.current_income_var.trace_add("write", lambda *_: self.update_calculated_fee())
        self.employment_mode_var.trace_add("write", lambda *_: self.update_calculated_fee())
        self.desired_service_var.trace_add("write", lambda *_: self.update_calculated_fee())
        self.structure_var.trace_add("write", lambda *_: self._on_structure_changed())

    def update_calculated_fee(self) -> None:
        """Automatically recalculates and updates the read-only affiliation fee field."""
        try:
            income = float(self.current_income_var.get().strip())
            fee = self.controller.calculate_fee(
                income,
                self.employment_mode_var.get(),
                self.desired_service_var.get(),
            )
            self.affiliation_fee_var.set(f"${fee:,.2f}")
        except ValueError:
            self.affiliation_fee_var.set("$0.00")

    def _on_structure_changed(self) -> None:
        """Refreshes the Treeview and clears the Report field when switching structures."""
        self.refresh_treeview()
        self.report_var.set("")
        self.status_var.set(
            f"Estructura activa: {self.structure_var.get()}. Presione 'Reporte' para consultar."
        )

    def refresh_treeview(self) -> None:
        """Populates the Treeview with the records of the currently selected structure."""
        for item_id in self.treeview.get_children():
            self.treeview.delete(item_id)

        structure = self.structure_var.get()
        banners = {
            "Pila": "Estructura Activa: Pila (LIFO — Apilar al tope / Desapilar último ingresado)",
            "Cola": "Estructura Activa: Cola (FIFO — Encolar al final / Desencolar primero ingresado)",
            "Lista": "Estructura Activa: Lista (Secuencial — Agregar al final / Eliminar por Número de ID)",
        }
        self.structure_banner_label.configure(
            text=banners.get(structure, f"Estructura Activa: {structure}")
        )

        for affiliate in self.controller.get_records(structure):
            self.treeview.insert(
                "",
                tk.END,
                iid=affiliate.id_number,
                values=affiliate.to_treeview_row(),
            )

    def _resolve_target_id_for_list(self) -> str:
        """Resolves the target ID number for deletion in the List structure."""
        typed_id = self.id_number_var.get().strip()
        if typed_id:
            return typed_id

        selected = self.treeview.selection()
        if selected:
            values = self.treeview.item(selected[0], "values")
            if values and len(values) >= 2:
                return str(values[1]).strip()

        self.id_number_entry.focus_set()
        raise ValueError(
            "Para eliminar en la estructura Lista, debe digitar primero el Número de Identificación del afiliado."
        )

    def handle_register(self) -> None:
        """Validates form fields, registers the affiliate, and updates the Treeview."""
        try:
            structure = self.structure_var.get()
            affiliate = self.controller.create_affiliate(
                id_type=self.id_type_var.get(),
                id_number=self.id_number_var.get(),
                full_name=self.full_name_var.get(),
                current_income_text=self.current_income_var.get(),
                desired_service=self.desired_service_var.get(),
                employment_mode=self.employment_mode_var.get(),
                affiliation_date_text=self.date_selector.get_date_string(),
            )
            self.controller.register_affiliate(structure, affiliate)
            self.refresh_treeview()
            self.handle_clear()
            self.status_var.set(
                f"Afiliado '{affiliate.full_name}' (ID {affiliate.id_number}) registrado en {structure}."
            )
        except ValueError as err:
            messagebox.showerror("Error de Validación", str(err), parent=self.root)

    def handle_delete(self) -> None:
        """Confirms with the user and deletes a record according to the active structure."""
        structure = self.structure_var.get()
        try:
            if not self.controller.get_records(structure):
                messagebox.showerror(
                    f"{structure} Vacía",
                    f"No hay registros en la {structure} para eliminar.",
                    parent=self.root,
                )
                return

            target_id: Optional[str] = None
            if structure == "Lista":
                target_id = self._resolve_target_id_for_list()

            target = self.controller.peek_for_deletion(structure, target_id)
            if target is None:
                messagebox.showerror(
                    "Afiliado No Encontrado",
                    f"No existe ningún afiliado con el Número de Identificación '{target_id}' en la Lista.",
                    parent=self.root,
                )
                return

            confirmed = messagebox.askyesno(
                f"Confirmar Eliminación ({structure})",
                f"¿Está seguro de eliminar el siguiente registro de la {structure}?\n\n"
                f"ID: {target.id_type} {target.id_number}\nNombre: {target.full_name}",
                parent=self.root,
            )
            if not confirmed:
                return

            removed = self.controller.delete_affiliate(structure, target_id)
            if structure == "Lista" and self.id_number_var.get().strip() == removed.id_number:
                self.id_number_var.set("")

            self.refresh_treeview()
            self.report_var.set("")
            self.status_var.set(
                f"Registro eliminado de {structure}: {removed.full_name} (ID {removed.id_number})."
            )
        except (ValueError, IndexError, LookupError) as err:
            messagebox.showerror("Error al Eliminar", str(err), parent=self.root)

    def handle_report(self) -> None:
        """Calculates and displays the report for the active structure in the Report field."""
        structure = self.structure_var.get()
        report_text = self.controller.generate_report_text(structure)
        self.report_var.set(report_text)
        self.status_var.set(f"Reporte generado ({structure}): {report_text}")

    def handle_clear(self) -> None:
        """Clears all capture fields without affecting the records in the Treeview."""
        self.id_type_var.set(ID_TYPES[0])
        self.id_number_var.set("")
        self.full_name_var.set("")
        self.current_income_var.set("")
        self.employment_mode_var.set(EMPLOYMENT_MODES[0])
        self.desired_service_var.set(DESIRED_SERVICES[0])
        self.affiliation_fee_var.set("$0.00")
        self.report_var.set("")
        self.date_selector.reset_to_today()
        self.id_number_entry.focus_set()
        self.status_var.set(
            "Campos del formulario limpiados. Los registros del Treeview se mantienen intactos."
        )

    def handle_exit(self) -> None:
        """Terminates application execution."""
        self.root.destroy()
