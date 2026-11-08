"""Formulario principal de captura, gestión de estructuras y reportes de afiliados (RF-02 a RF-05)."""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from typing import Optional

from src.config.constants import (
    COURSE_CODE,
    COURSE_NAME,
    DATA_STRUCTURES,
    DESIRED_SERVICES,
    EMPLOYMENT_EMPLOYEE,
    EMPLOYMENT_INDEPENDENT,
    ID_TYPES,
    MAIN_WINDOW_TITLE,
    SERVICE_UNEMPLOYMENT_SUBSIDY,
    STRUCTURE_LIST,
    STRUCTURE_QUEUE,
    STRUCTURE_STACK,
    STUDENT_NAME,
)
from src.domain.data_structures import AffiliateRepository
from src.presentation.formatters import format_affiliate_treeview_row, format_currency
from src.presentation.theme import (
    ACCENT_AMBER,
    ACCENT_CYAN,
    ACCENT_GREEN,
    ACCENT_RED,
    ACCENT_SLATE,
    BG_CARD,
    BG_INPUT,
    BG_PRIMARY,
    BG_SECONDARY,
    FG_PRIMARY,
    FG_SECONDARY,
    FONT_FAMILY,
    apply_application_theme,
)
from src.presentation.widgets.date_entry_spinbox import DateEntrySpinbox
from src.services.data_validation_service import DataValidationService
from src.services.fee_calculator_service import FeeCalculatorService
from src.services.report_service import ReportService


class AffiliateForm:
    """Ventana principal 'Caja Compensándote – Control de Afiliados'."""

    def __init__(
        self,
        root: tk.Tk,
        repository: Optional[AffiliateRepository] = None,
    ) -> None:
        self.root = root
        self.repository = repository if repository is not None else AffiliateRepository()

        # Variables reactivas del formulario
        self.id_type_var = tk.StringVar(value=ID_TYPES[0])
        self.id_number_var = tk.StringVar()
        self.full_name_var = tk.StringVar()
        self.current_income_var = tk.StringVar()
        self.employment_mode_var = tk.StringVar(value=EMPLOYMENT_EMPLOYEE)
        self.desired_service_var = tk.StringVar(value=SERVICE_UNEMPLOYMENT_SUBSIDY)
        self.affiliation_fee_var = tk.StringVar(value="$0.00")
        self.structure_type_var = tk.StringVar(value=STRUCTURE_STACK)
        self.report_var = tk.StringVar(
            value=ReportService.generate_report_text(STRUCTURE_STACK, self.repository)
        )
        self.status_var = tk.StringVar(
            value="Listo — Diligencie el formulario y presione 'Registrar'."
        )

        self._configure_window()
        self._build_ui()
        self._bind_reactive_calculation()
        self.refresh_treeview()
        self.id_number_entry.focus_set()

    def _configure_window(self) -> None:
        """Configura geometría, título y estilo de la ventana principal."""
        apply_application_theme(self.root)
        self.root.title(MAIN_WINDOW_TITLE)
        self.root.configure(bg=BG_PRIMARY)
        self.root.resizable(True, True)

        width = 1200
        height = 730
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        pos_x = max(0, (screen_width - width) // 2)
        pos_y = max(0, (screen_height - height) // 2)
        self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        self.root.minsize(1040, 660)

    def _build_ui(self) -> None:
        """Construye el diseño de dos columnas: formulario de captura y tabla Treeview."""
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
        """Construye el panel izquierdo con los campos de captura y validación."""
        panel = tk.Frame(
            parent,
            bg=BG_SECONDARY,
            padx=14,
            pady=10,
            highlightbackground=BG_CARD,
            highlightthickness=1,
        )
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        vcmd_digits = (
            self.root.register(DataValidationService.is_valid_realtime_digits),
            "%P",
        )
        vcmd_alpha = (
            self.root.register(DataValidationService.is_valid_realtime_alphabetic),
            "%P",
        )
        vcmd_decimal = (
            self.root.register(DataValidationService.is_valid_realtime_decimal),
            "%P",
        )

        # Sección 1: Identificación del Afiliado
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
            invalidcommand=lambda: self.status_var.set(
                "Aviso: El Número de Identificación solo acepta dígitos numéricos (máx. 15)."
            ),
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
            text="Nombre Completo (solo letras y espacios):",
            style="Field.TLabel",
        ).pack(fill=tk.X, pady=(2, 2))
        self.full_name_entry = tk.Entry(
            panel,
            textvariable=self.full_name_var,
            validate="key",
            validatecommand=vcmd_alpha,
            invalidcommand=lambda: self.status_var.set(
                "Aviso: El Nombre Completo solo acepta letras y espacios simples."
            ),
            bg=BG_INPUT,
            fg=FG_PRIMARY,
            insertbackground=FG_PRIMARY,
            relief="solid",
            bd=1,
            font=(FONT_FAMILY, 10),
        )
        self.full_name_entry.pack(fill=tk.X, ipady=3, pady=(0, 8))

        # Sección 2: Datos Económicos y Servicio
        ttk.Label(panel, text="2. Datos Económicos y Servicio", style="Section.TLabel").pack(
            fill=tk.X, pady=(2, 4)
        )

        ttk.Label(
            panel,
            text="Ingresos Actuales ($) (sin puntos de miles, mín. 1000000):",
            style="Field.TLabel",
        ).pack(fill=tk.X, pady=(2, 2))
        self.current_income_entry = tk.Entry(
            panel,
            textvariable=self.current_income_var,
            validate="key",
            validatecommand=vcmd_decimal,
            invalidcommand=lambda: self.status_var.set(
                "Aviso: Digite los Ingresos Actuales solo con números (sin puntos de miles)."
            ),
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
        self.employee_radio = ttk.Radiobutton(
            radio_frame,
            text=EMPLOYMENT_EMPLOYEE,
            variable=self.employment_mode_var,
            value=EMPLOYMENT_EMPLOYEE,
        )
        self.employee_radio.pack(side=tk.LEFT, padx=(0, 16))
        self.independent_radio = ttk.Radiobutton(
            radio_frame,
            text=EMPLOYMENT_INDEPENDENT,
            variable=self.employment_mode_var,
            value=EMPLOYMENT_INDEPENDENT,
        )
        self.independent_radio.pack(side=tk.LEFT)

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

        # Sección 3: Fecha de Afiliación (DateEntry + Spinbox)
        ttk.Label(
            panel,
            text="3. Fecha de Afiliación (DateEntry + Spinbox)",
            style="Section.TLabel",
        ).pack(fill=tk.X, pady=(2, 4))
        self.date_selector = DateEntrySpinbox(panel)
        self.date_selector.pack(fill=tk.X, pady=(0, 8))

        # Sección 4: Estructura de Datos y Reporte
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
            textvariable=self.structure_type_var,
            values=DATA_STRUCTURES,
            state="readonly",
        )
        self.structure_combo.pack(fill=tk.X, pady=(0, 6))
        self.structure_combo.bind("<<ComboboxSelected>>", self._on_structure_changed)

        ttk.Label(
            panel,
            text="Reporte — no editable:",
            style="Field.TLabel",
        ).pack(fill=tk.X, pady=(2, 2))
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

        for entry in (
            self.id_number_entry,
            self.full_name_entry,
            self.current_income_entry,
        ):
            entry.bind("<Return>", lambda _e: self.handle_register())

    def _build_right_panel(self, parent: tk.Frame) -> None:
        """Construye el panel derecho con la tabla Treeview y los 5 botones de acción."""
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

        column_specs = (
            ("id_type", "Tipo ID", 65, "center"),
            ("id_number", "Número ID", 105, "center"),
            ("full_name", "Nombre Completo", 175, "w"),
            ("current_income", "Ingresos ($)", 115, "e"),
            ("desired_service", "Servicio Deseado", 150, "w"),
            ("employment_mode", "Modalidad", 100, "center"),
            ("affiliation_fee", "Tarifa ($)", 105, "e"),
            ("affiliation_date", "Fecha Afiliación", 105, "center"),
        )
        for col_id, heading_text, width, anchor in column_specs:
            self.treeview.heading(col_id, text=heading_text)
            self.treeview.column(
                col_id,
                width=width,
                minwidth=width,
                anchor=anchor,
                stretch=True,
            )

        v_scroll = ttk.Scrollbar(
            tree_frame,
            orient=tk.VERTICAL,
            command=self.treeview.yview,
        )
        h_scroll = ttk.Scrollbar(
            tree_frame,
            orient=tk.HORIZONTAL,
            command=self.treeview.xview,
        )
        self.treeview.configure(
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set,
        )

        self.treeview.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        self.treeview.bind("<Delete>", lambda _e: self.handle_delete())

        # Barra inferior de botones: Registrar, Eliminar, Reporte, Limpiar y Salir
        actions_frame = tk.Frame(right_panel, bg=BG_PRIMARY, pady=10)
        actions_frame.grid(row=2, column=0, sticky="ew")
        actions_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

        button_configs = (
            ("Registrar", self.handle_register, ACCENT_CYAN, 0),
            ("Eliminar", self.handle_delete, ACCENT_RED, 1),
            ("Reporte", self.handle_report, ACCENT_GREEN, 2),
            ("Limpiar", self.handle_clear, ACCENT_AMBER, 3),
            ("Salir", self.handle_exit, ACCENT_SLATE, 4),
        )
        for text, command, color, col_idx in button_configs:
            btn = tk.Button(
                actions_frame,
                text=text,
                command=command,
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

    def _bind_reactive_calculation(self) -> None:
        """Enlaza cambios de ingresos, modalidad, servicio y estructura con la interfaz."""
        self.current_income_var.trace_add("write", lambda *_: self._update_calculated_fee())
        self.employment_mode_var.trace_add("write", lambda *_: self._update_calculated_fee())
        self.desired_service_var.trace_add("write", lambda *_: self._update_calculated_fee())
        self.structure_type_var.trace_add("write", lambda *_: self._on_structure_changed())

    def _update_calculated_fee(self) -> None:
        """Recalcula y muestra automáticamente la tarifa cuando los datos son válidos."""
        valid_income = DataValidationService.try_parse_valid_income(
            self.current_income_var.get()
        )
        if valid_income is None:
            self.affiliation_fee_var.set("$0.00")
            return

        employment_mode = self.employment_mode_var.get().strip()
        desired_service = self.desired_service_var.get().strip()
        if (
            employment_mode not in (EMPLOYMENT_EMPLOYEE, EMPLOYMENT_INDEPENDENT)
            or desired_service not in DESIRED_SERVICES
        ):
            self.affiliation_fee_var.set("$0.00")
            return

        fee = FeeCalculatorService.calculate_fee(
            current_income=valid_income,
            employment_mode=employment_mode,
            desired_service=desired_service,
        )
        self.affiliation_fee_var.set(format_currency(fee))

    def _on_structure_changed(self, _event: object = None) -> None:
        """Actualiza el Treeview y el reporte al cambiar entre Pila, Cola y Lista."""
        structure = self.structure_type_var.get().strip()
        if structure not in DATA_STRUCTURES:
            return
        self.refresh_treeview()
        self.report_var.set(
            ReportService.generate_report_text(structure, self.repository)
        )
        self.status_var.set(f"Estructura visualizada cambiada a: {structure}.")

    def refresh_treeview(self) -> None:
        """Sincroniza las filas del Treeview con los registros de la estructura activa."""
        children = self.treeview.get_children()
        if children:
            self.treeview.delete(*children)

        structure = self.structure_type_var.get()
        descriptions = {
            STRUCTURE_STACK: "Estructura Activa: Pila (LIFO — Apilar al tope / Desapilar último ingresado)",
            STRUCTURE_QUEUE: "Estructura Activa: Cola (FIFO — Encolar al final / Desencolar primero ingresado)",
            STRUCTURE_LIST: "Estructura Activa: Lista (Secuencial — Agregar al final / Eliminar por Número de ID)",
        }
        self.structure_banner_label.configure(
            text=descriptions.get(structure, f"Estructura Activa: {structure}")
        )

        for affiliate in self.repository.get_structure(structure):
            self.treeview.insert(
                "",
                tk.END,
                iid=affiliate.id_number,
                values=format_affiliate_treeview_row(affiliate),
            )

    def _reset_capture_fields(self) -> None:
        """Limpia los controles de captura sin alterar los datos del Treeview."""
        self.id_type_var.set(ID_TYPES[0])
        self.id_number_var.set("")
        self.full_name_var.set("")
        self.current_income_var.set("")
        self.employment_mode_var.set(EMPLOYMENT_EMPLOYEE)
        self.desired_service_var.set(SERVICE_UNEMPLOYMENT_SUBSIDY)
        self.affiliation_fee_var.set("$0.00")
        self.date_selector.reset_to_today()
        self.id_number_entry.focus_set()

    def handle_register(self) -> None:
        """Valida los datos e inserta el afiliado en la estructura seleccionada."""
        try:
            structure_type = DataValidationService.validate_structure_type(
                self.structure_type_var.get()
            )
            affiliate = DataValidationService.validate_and_create_affiliate(
                id_type=self.id_type_var.get(),
                id_number=self.id_number_var.get(),
                full_name=self.full_name_var.get(),
                current_income_text=self.current_income_var.get(),
                desired_service=self.desired_service_var.get(),
                employment_mode=self.employment_mode_var.get(),
                affiliation_date_text=self.date_selector.get_date_string(),
            )

            self.repository.add_affiliate(structure_type, affiliate)
            self.refresh_treeview()
            self.report_var.set(
                ReportService.generate_report_text(structure_type, self.repository)
            )
            self._reset_capture_fields()
            self.status_var.set(
                f"Afiliado '{affiliate.full_name}' (ID {affiliate.id_number}) registrado exitosamente en {structure_type}."
            )
        except ValueError as err:
            messagebox.showerror(
                "Error de Validación",
                str(err),
                parent=self.root,
            )

    def _resolve_target_id_for_list_deletion(self) -> Optional[str]:
        """Obtiene el ID a eliminar en Lista desde el campo de texto, selección o cuadro de diálogo."""
        typed_id = self.id_number_var.get().strip()
        if typed_id:
            return typed_id

        selected_items = self.treeview.selection()
        if selected_items:
            row_values = self.treeview.item(selected_items[0], "values")
            if row_values and len(row_values) >= 2:
                return str(row_values[1]).strip()

        prompted_id = simpledialog.askstring(
            "Eliminar de la Lista",
            "Digite el Número de Identificación del afiliado a eliminar:",
            parent=self.root,
        )
        if prompted_id is None:
            return None
        return prompted_id.strip()

    def handle_delete(self) -> None:
        """Elimina un registro según la estructura activa previa confirmación del usuario."""
        try:
            structure_type = DataValidationService.validate_structure_type(
                self.structure_type_var.get()
            )

            if self.repository.is_structure_empty(structure_type):
                empty_titles = {
                    STRUCTURE_STACK: ("Pila Vacía", "No hay registros en la Pila para desapilar."),
                    STRUCTURE_QUEUE: ("Cola Vacía", "No hay registros en la Cola para desencolar."),
                    STRUCTURE_LIST: ("Lista Vacía", "No hay registros en la Lista para eliminar."),
                }
                title, msg = empty_titles[structure_type]
                messagebox.showerror(title, msg, parent=self.root)
                return

            target_id: Optional[str] = None
            if structure_type == STRUCTURE_LIST:
                raw_target_id = self._resolve_target_id_for_list_deletion()
                if raw_target_id is None:
                    return
                target_id = DataValidationService.validate_id_number(raw_target_id)

            target_affiliate = self.repository.peek_target_for_deletion(
                structure_type,
                target_id=target_id,
            )
            if target_affiliate is None:
                messagebox.showerror(
                    "Afiliado No Encontrado",
                    f"No existe ningún afiliado con el Número de Identificación '{target_id}' en la Lista.",
                    parent=self.root,
                )
                return

            action_descriptions = {
                STRUCTURE_STACK: (
                    "Confirmar Eliminación (Pila - Desapilar)",
                    "¿Está seguro de desapilar el último registro ingresado?",
                ),
                STRUCTURE_QUEUE: (
                    "Confirmar Eliminación (Cola - Desencolar)",
                    "¿Está seguro de desencolar el primer registro ingresado?",
                ),
                STRUCTURE_LIST: (
                    "Confirmar Eliminación (Lista)",
                    "¿Está seguro de eliminar el siguiente afiliado de la Lista?",
                ),
            }
            dialog_title, dialog_question = action_descriptions[structure_type]
            confirmed = messagebox.askyesno(
                dialog_title,
                f"{dialog_question}\n\n"
                f"ID: {target_affiliate.id_type} {target_affiliate.id_number}\n"
                f"Nombre: {target_affiliate.full_name}",
                parent=self.root,
            )
            if not confirmed:
                return

            removed = self.repository.remove_affiliate(
                structure_type,
                target_id=target_id,
            )
            if structure_type == STRUCTURE_LIST and self.id_number_var.get().strip() == removed.id_number:
                self.id_number_var.set("")

            self.refresh_treeview()
            self.report_var.set(
                ReportService.generate_report_text(structure_type, self.repository)
            )
            self.status_var.set(
                f"Registro eliminado de {structure_type}: {removed.full_name} (ID {removed.id_number})."
            )
        except (ValueError, IndexError, LookupError) as err:
            messagebox.showerror(
                "Error al Eliminar",
                str(err),
                parent=self.root,
            )

    def handle_report(self) -> None:
        """Calcula y muestra el reporte estadístico de la estructura seleccionada."""
        try:
            structure_type = DataValidationService.validate_structure_type(
                self.structure_type_var.get()
            )
            report_text = ReportService.generate_report_text(
                structure_type=structure_type,
                repository=self.repository,
            )
            self.report_var.set(report_text)
            self.status_var.set(f"Reporte generado para {structure_type}: {report_text}")
        except ValueError as err:
            messagebox.showerror(
                "Error en Reporte",
                str(err),
                parent=self.root,
            )

    def handle_clear(self) -> None:
        """Limpia los campos del formulario sin afectar los registros del Treeview."""
        self._reset_capture_fields()
        self.status_var.set(
            "Campos del formulario limpiados. Los registros de las estructuras se mantienen intactos."
        )

    def handle_exit(self) -> None:
        """Finaliza la ejecución de la aplicación."""
        self.root.destroy()
