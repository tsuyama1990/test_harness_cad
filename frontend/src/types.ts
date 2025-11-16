export interface LibraryComponent {
  id: string;
  type: 'connector' | 'wire';
  name: string;
  data: Record<string, unknown>;
}
